import os
import csv
import json
import math
import shutil
import argparse
import numpy as np
import tensorflow as tf
from pathlib import Path
from datetime import datetime
from azureml.core.run import Run
from amlcallback import AMLCallback
from tensorflow.keras.callbacks import ModelCheckpoint

# Create a dictionary describing the features.
image_feature_description = {
    'height': tf.io.FixedLenFeature([], tf.int64),
    'width': tf.io.FixedLenFeature([], tf.int64),
    'depth': tf.io.FixedLenFeature([], tf.int64),
    'label': tf.io.FixedLenFeature([], tf.int64),
    'image': tf.io.FixedLenSequenceFeature([], tf.float32, allow_missing=True),
}

def info(msg, char = "#", width = 75):
    print("")
    print(char * width)
    print(char + "   %0*s" % ((-1*width)+5, msg) + char)
    print(char * width)

def split(records, split=[8, 1, 1]):
    # normalize splits
    splits = np.array(split) / np.sum(np.array(split))
    # split data
    train_idx = int(len(records) * splits[0])
    eval_idx = int(len(records) * splits[1])
    
    return records[:train_idx], \
            records[train_idx:train_idx + eval_idx + 1], \
            records[train_idx + eval_idx + 1:]

def parse_record(example_proto):
    # Parse the input tf.Example proto using the dictionary above.
    example = tf.io.parse_single_example(example_proto, image_feature_description)
    shape = [example['height'], 
             example['width'], 
             example['depth']]
    
    label = example['label']
    image = tf.reshape(example['image'], shape)
    return (image, label)


def main(run, data_path, output_path, target_output, epochs, batch, lr):
    info('Preprocess')
    # load tfrecord metadata
    prep_step = os.path.join(output_path, 'prep.json')
    with open(prep_step) as f:
        prep = json.load(f)

    for i in prep:
        print('{} => {}'.format(i, prep[i]))

    labels = prep['categories']
    img_shape = (prep['image_size'], prep['image_size'], 3)
    record_sz = prep['records']

    records = os.path.join(data_path, prep['file'])
    print('Loading {}'.format(records))
    with open(records, 'r') as f:
        filenames = [os.path.join(data_path, s.strip()) for s in f.readlines()]
    
    print('Splitting data:')
    train, test, val = split(filenames)
    print('  Train: {}'.format(len(train)))
    print('   Test: {}'.format(len(test)))
    print('    Val: {}'.format(len(val)))

    print('Creating training dataset')
    train_ds = tf.data.TFRecordDataset(train)
    train_ds = train_ds.map(map_func=parse_record, num_parallel_calls=5)
    train_ds = train_ds.shuffle(buffer_size=10000)
    train_ds = train_ds.batch(batch)
    train_ds = train_ds.prefetch(buffer_size=5)
    train_ds = train_ds.repeat(epochs)

    # model
    info('Creating Model')
    #base_model = tf.keras.applications.MobileNetV2(input_shape=img_shape,
    #                                           include_top=False, 
    #                                           weights='imagenet',
    #                                           pooling='avg')

    base_model = tf.keras.applications.VGG19(input_shape=img_shape,
                                               include_top=False, 
                                               weights='imagenet',
                                               pooling='avg')

    base_model.trainable = True

    model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.Dense(len(labels), activation='softmax')
    ])

    model.compile(optimizer=tf.keras.optimizers.Adam(lr=lr), 
              loss='sparse_categorical_crossentropy', 
              metrics=['accuracy'])

    model.summary()
    
    # training
    info('Training')

    # callbacks
    logaml = AMLCallback(run)
    filename = datetime.now().strftime("%d.%b.%Y.%H.%M")
    model_path = os.path.join(target_output, 'model')
    if not os.path.exists(model_path):
        os.makedirs(model_path)
    checkpoint = ModelCheckpoint(os.path.join(model_path, filename + '.e{epoch:02d}-{accuracy:.2f}.hdf5'))


    test_ds = tf.data.TFRecordDataset(test).map(parse_record).batch(batch)
    test_steps = math.ceil((len(test)*record_sz)/batch)

    steps_per_epoch = math.ceil((len(train)*record_sz)/batch)
    history = model.fit(train_ds, 
                    epochs=epochs, 
                    steps_per_epoch=steps_per_epoch,
                    callbacks=[logaml, checkpoint],
                    validation_data=test_ds,
                    validation_steps=test_steps)

    print('Done!')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='data cleaning for binary image task')
    parser.add_argument('-d', '--data_path', help='directory to training data', default='data')
    parser.add_argument('-o', '--output_path', help='directory to previous data step', default='data')
    parser.add_argument('-t', '--target_output', help='target file to hold data', default='data')
    parser.add_argument('-e', '--epochs', help='number of epochs', default=10, type=int)
    parser.add_argument('-b', '--batch', help='batch size', default=32, type=int)
    parser.add_argument('-l', '--lr', help='learning rate', default=0.0001, type=float)
    args = parser.parse_args()

    run = Run.get_context()
    offline = run.id.startswith('OfflineRun')
    print('AML Context: {}'.format(run.id))
    

    info('Input Arguments')
    params = vars(args)
    for i in params:
        print('{} => {}'.format(i, params[i]))

    # log output
    if not offline:
        for item in args:
            if item != 'run':
                run.log(item, args[item])

    params['run'] = run

    main(**params)