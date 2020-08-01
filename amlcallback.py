import tensorflow as tf


class AMLCallback(tf.keras.callbacks.Callback):

    def __init__(self, run):
        self.run = run

    def on_train_end(self, logs=None):
        if logs != None:
            for k in logs.keys():
                self.run.log(f'final_{k}', logs[k])

    def on_epoch_end(self, epoch, logs=None):
        if logs != None:
            for k in logs.keys():
                self.run.log(f'epoch_{k}', logs[k])

    def on_train_batch_end(self, batch, logs=None):
        if logs != None:
            for k in logs.keys():
                self.run.log(f'{k}', logs[k])
