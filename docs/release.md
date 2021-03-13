# Creating a Release Pipeline
There are a couple of steps to get this done:
1. Deploy the [mlrouter](https://github.com/cloudscaleml/mlrouter) Azure Function
    - There are couple of things hard coded in the function (`ghUri` needs to be changed to your particular repo).
    - The job of this Azure Function is to take Event Grid messages from your Machine Learning Workspace and relay them back to GitHub by triggering a `repository_dispatch` event to the [deploy](../.github/worflows/deploy.yml) GH Action. This takes the registered model and deploys the correct scoring code to AML in order to create an inference endpoint.
2. Open up you AML worspace in the _Azure_ portal (not the ml portal), select `Events`, and create a new Event Subscription
3. Give it a name and choose the Azure Function Endpoint Type (the rest of the params can be left alone)
4. Select the Azure Function you just deployed in Step 1.
5. To make this all work you can either check in a newer version of the code or re-run the pipeline in AML studio. At the end of the Pipeline run the workspace Event Grid will notify GitHub that the model has been registered. The [deploy](../.github/worflows/deploy.yml) GH Action should deploy the model to your workspace and create an endpoint.
