# Setting up your Azure Machine Learning Datstore
1. Download the [image files](https://aiadvocate.blob.core.windows.net/public/tacosburrito.zip)
2. Create a container in your workspace attached storage account (this can be done using the [Azure Storage Explorer](https://azure.microsoft.com/en-us/features/storage-explorer/))
3. Create a folder in the newly created container.
4. Upload the `burrito` and `tacos` folder into the newly created folder
5. Remember how you named things (both the `container` AND the `path`)
6. In your AzureML Workspace navigate over to Datasets.
7. Add a new Dataset by selecting the appropriate storage account and Blob Container.
8. Fill in the Storage Account Key by retrieving it from the Storage Resource (this is found under `Access Keys` in the Storage Account Blade)
9. Remember the name of the new `Dataset`
