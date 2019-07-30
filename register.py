import os
import json
import azureml
import argparse
from pathlib import Path
from azureml.core.run import Run
from azureml.core import Workspace
from azureml.core.model import Model
from azureml.core.image import ContainerImage, Image
from azureml.core.webservice import Webservice, AciWebservice
from azureml.core.authentication import ServicePrincipalAuthentication 

def info(msg, char = "#", width = 75):
    print("")
    print(char * width)
    print(char + "   %0*s" % ((-1*width)+5, msg) + char)
    print(char * width)

def main(run, models):

    print(run.workspace)
    # Model Path needs to be relative
    #model_path = relpath(model_path, '.')

    #model = Model.register(ws, model_name=model_name, model_path=model_path, tags=tags)
    print('Done!')

if __name__ == "__main__":
    # argparse stuff for model path and model name
    parser = argparse.ArgumentParser(description='Model Registration Process')
    parser.add_argument('-m', '--models', help='path to model file', default='data/train')
    args = parser.parse_args()

    run = Run.get_context()
    offline = run.id.startswith('OfflineRun')
    print('AML Context: {}'.format(run.id))
    
    info('Input Arguments')
    params = vars(args)
    for i in params:
        print('{} => {}'.format(i, params[i]))
        if not offline:
            run.log(i, params[i])

    params['run'] = run

    main(**params)
