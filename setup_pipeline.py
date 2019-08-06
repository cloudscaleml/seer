from azureml.core import Workspace, Experiment, Datastore
from azureml.data.datapath import DataPath, DataPathComputeBinding
from azureml.data.data_reference import DataReference
from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.pipeline.core import Pipeline, PipelineData, PipelineParameter
from azureml.pipeline.steps import PythonScriptStep, EstimatorStep
from azureml.widgets import RunDetails
from azureml.train.estimator import Estimator
import os

# Get environment variables
datastorename=os.environ('datastorename')
containername=os.environ('containername')
accountname=os.environ('accountname')
accountkey=os.environ('storageaccountkey')
datastorepath=os.environ('datapath')
computetarget=os.environ('computetarget')

print("Azure ML SDK Version: ", azureml.core.VERSION)

# workspace
ws = Workspace.from_config(
    path='./azureml-config.json')
ws.datastores

# data
datastore = ws.datastores[datastorename]
if datastore is None:
    datastore = Datastore.register_azure_blob_container(workspace=ws, 
                                                datastore_name=datastorename, 
                                                container_name=containername,
                                                account_name=accountname, 
                                                account_key=accountkey,
                                                create_if_not_exists=False)


# compute target
compute = ws.compute_targets[computetarget]

# # Define Pipeline!
# The following will be created and then run:
# 1. Pipeline Parameters
# 2. Data Fetch Step
# 3. Data Process Step
# 4. Model Registration Step
# 5. Training Step
# 

# ## Pipeline Parameters
# We need to tell the Pipeline what it needs to learn to see!

datapath = DataPath(datastore=datastore, path_on_datastore='hardware')
data_path_pipeline_param = (PipelineParameter(name="data", 
                                             default_value=datastorepath), 
                                             DataPathComputeBinding(mode='mount'))
data_path_pipeline_param


# ## Data Process Step

seer_tfrecords = PipelineData(
    "tfrecords_set",
    datastore=datastore,
    is_directory=True
)

prep = Estimator(source_directory='.',
                      compute_target=compute,
                      entry_script='parse.py',
                      use_gpu=True,
                      pip_requirements_file='requirements.txt')

prepStep = EstimatorStep(
    name='Data Preparation',
    estimator=prep,
    estimator_entry_script_arguments=["--source_path", data_path_pipeline_param, 
                                      "--target_path", seer_tfrecords],
    inputs=[data_path_pipeline_param],
    outputs=[seer_tfrecords],
    compute_target=compute
)

# ## Training Step

seer_training = PipelineData(
    "train",
    datastore=datastore,
    is_directory=True
)

train = Estimator(source_directory='.',
                      compute_target=compute,
                      entry_script='train.py',
                      use_gpu=True,
                      pip_requirements_file='requirements.txt')

trainStep = EstimatorStep(
    name='Model Training',
    estimator=train,
    estimator_entry_script_arguments=["--source_path", seer_tfrecords, 
                                      "--target_path", seer_training,
                                      "--epochs", 5,
                                      "--batch", 10,
                                      "--lr", 0.001],
    inputs=[seer_tfrecords],
    outputs=[seer_training],
    compute_target=compute
)

# # Register Model Step

seer_model = PipelineData(
    "model",
    datastore=datastore,
    is_directory=True
)

register = Estimator(source_directory='.',
                      compute_target=compute,
                      entry_script='register.py',
                      use_gpu=True)

registerStep = EstimatorStep(
    name='Model Registration',
    estimator=register,
    estimator_entry_script_arguments=["--source_path", seer_training, 
                                      "--target_path", seer_model],
    inputs=[seer_training],
    outputs=[seer_model],
    compute_target=compute
)

# ## Create and publish the Pipeline

pipeline = Pipeline(workspace=ws, steps=[prepStep, trainStep, registerStep])

published_pipeline = pipeline.publish(
    name="Seer Pipeline", 
    description="Transfer learned image classifier. Uses folders as labels.")

# Submit the pipeline to be run
pipeline_run = Experiment(ws, 'seer').submit(pipeline)
#RunDetails(pipeline_run).show()

print('Run created with ID: ', pipeline_run.run_id)