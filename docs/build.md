# Building and Running an AML Pipeline
The goal of this exercise is to rebuild and run an AML pipeline every time code is changed in the repo.
Hopefully at this point you have forked this repo. After that we will proceed as follows:


1. Create an Azure DevOps Organization (or open it up if there is an existing one)
2. Add the AzureML DevOps Extension
3. Create a new Project
4. Create Build Pipeline
5. Create Service Connections
6. Create build variables (in a variable group)
7. Run the build!

## Create an Azure DevOps Organization
If you haven't already you can create a free instance of Azure Devops by going to [dev.azure.com](https://dev.azure.com). Feel free to look around (there's a lot you can do with it).

## Add AzureML DevOps Extension
Under `Organization Settings` navigate over to `Extensions`. Click on `Browse Marketplace` and search for `Machine Learning`. You should find [Machine Learning](https://marketplace.visualstudio.com/items?itemName=ms-air-aiagility.vss-services-azureml) extension. Click on [Get it Free](https://marketplace.visualstudio.com/acquisition?itemName=ms-air-aiagility.vss-services-azureml) to install.

## Create a new Project
Once you have your organization set up we need to create a new project where all the magic will happen. You can name it whatever you like!

## Create Build Pipeline
Steps for creating a build pipeline:
1. Navigate over to Pipelines\Buils
2. Click on `+New` to create a new build
3. Select Github as your code repository (hopefully you have already forked the main repository)
4. Select the forked repository that contains all of the `seer` code
5. During the configuration step choose "Existing Azure Pipelines YAML file`
6. Choose `/azure-pipelines.yml`

Take a moment to look around at all of the steps to get familiar with what the pipeline attempts to accomplish. Attempting to queue up the pipeline will fail however given there's some Service Connections and variables we need to set up in order to make everything work!

## Create Service Connections
Service connections grant Azure DevOps access to Azure resources. For this project we need 2:
1. Access to the resource group
2. Access to the Azure Machine Learning workspace

Click on `Project Settings` and navigate to `Pipelines\Service Connections`. We will crate the service connections we need here.

### Resource Group Connection
Click on `+New Service Connection` and choose `ARM Resource Manager`. Set Scope Level to `Subscription` and choose the appropriate Subscription and Resource Group. You can call it whatever you like (but it will have reprecusions). In our case we chose `seer`. Click `OK` to create the service connection

### Azure Machine Learning workspace Connection
Follow the same steps as above but instead set the Scope Level to `AzureMLWorkspace`. You can call it whatever you like (but it will have reprecusions). In our case we chose `seerws`. Click `OK` to create the service connection

## Create Build Variables
Use the following steps to set up the appropriate build variables:

1. Navigate over to Pipelines\Library
2. Create a new variable group called `seer-variables`
3. Fill in the following variables:

|Variable | Description |
|---------|--------------------
|access_token| This will be used later on during the release phase. You can get a PAT by following some additional [instructions](https://docs.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops&viewFallbackFrom=vsts&tabs=preview-page#create-personal-access-tokens-to-authenticate-access).
|computetarget| This is the name of your AzureML Compute Target |
|datastorename| This is the name of the datastore you've created that points to your tacos and burritos. Make sure this is [set up](datastore.md) beforehand. |
|datastorepath| Your datastore will point to a container. This value represents the sub directory where the actual images live. |
|org_name| This is the name of your DevOps organization |
|resource_group| This represents the resource group where you AzureML studio account lives|
|storage_account| This represents the name of your storage account |
|subscription| `seer` if you used this name for the Resource Group Service Connection|
|subscription_workspace| `seerws` if you used this name for the AzureML Workspace Service Connection|
|workspace| This represents the name of your workspace |

Make sure to turn the toggle to `Allow Access to all pipelines` to `On`

## Run the Build!
Navigate back to the build pipeline created earlier and Queue the Build!

A word about all of this: it will likely not work the first time (if it does you are a magician and I need to learn your ways). If it breaks it is totally ok - take a look at the output of the build to investigate what the problems might be and try again.