# Creating a Release Pipeline
There are a couple of steps to get this done:
1. Create a new release pipeline by navigating over to Pipelines\Builds and clicking on `+New` -> `+New Release Pipeline`
2. Select `Empty job` to start
3. Click on `Add Artifact` and select `AzureML Model Artifact` (you might have to click on `more`)
4. Select the service endpoint created in the [Build](build.md) instructions (in my case it is `seerws`) and the corresponding model
5. Click on the `View Stage Tasks` under `Stage` (it will have something like `1 job, 0 tasks`)
6. Click on Agent Job and change the Agent Specification to `ubuntu-18.04`
7. Click `+` on the Agent Job and add a `Azure CLI` task, Name it `Get Universal Package Version`, choose the appropriate Service Connection to the Resource Group, change the Script Location to Inline Script, and add the following to the Inline Script box:

```
echo "Retrieving universal package version for model $(Release.Artifacts._seer.DefinitionName):$(Release.Artifacts._seer.BuildNumber)"

modelId="$(Release.Artifacts._seer.DefinitionName):$(Release.Artifacts._seer.BuildNumber)"
pkgver=$(az ml model show -i $modelId -w $(workspace) -g $(resource_group) --query 'tags.uver' -o tsv)

echo "Universal Packages version is $pkgver"

echo "##vso[task.setvariable variable=UniversalPackageId]$pkgver"
```
8. Repeat the process but name it `Download Universal Package Files` and use the following:
```
az extension add -n azure-devops

echo "Retrieving Universal Package contents"
az artifacts universal download --organization "https://dev.azure.com/$(org_name)/" --scope project --project "b9fe7676-fda5-4c73-9547-3b59392c8e52" --feed "SeerInference" --name "seer_deployment" --version "$(UniversalPackageId)" --path $(System.DefaultWorkingDirectory)/deploymentcode
```
__NOTE__: You will have to change your project GUID. If you go to Artifacts and click on one of the Seer Deployments you will find the appropriate project GUID

9. Add `AZURE_DEVOPS_EXT_PAT` as an environment variable in this task and set it to `$(access_token)`

10. Add an `Azure ML Model Deploy` task
11. Add the correct Azure ML Workspace Service Connection
12. Use `$(System.DefaultWorkingDirectory)/deploymentcode/inferenceconfig.json` as the Inference Config Path
13. Under Deployment Information use Azure Container Instance  as the Model Deploymenty Target, `seer-deployment` as the Deployment Name, and `$(System.DefaultWorkingDirectory)/deploymentcode/deployconfig.json` as the deployment configuration file. 
14. Save the Release Pipeline
15. Click on the Pipeline Tab and enable the Continuous deployment trigger by clicking on the lightning bolt on the seer artifact.
16. Trigger a release to see if it works!

__NOTE__: It likely won't work the first time. That's totally ok. This likely means a variable was misconfigured or something else went awry. The output should be fairly helpful.

Now that all of this has been set up, every time you make a change to the repo the model will get rebuilt and deployed.

While this particular setup is not the ideal approach, his exercise is designed to inspire you as to the kinds of things that _can_ be done - not necessarily what _should_ be done.