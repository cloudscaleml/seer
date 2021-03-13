# Building and Running an AML Pipeline
The goal of this exercise is to rebuild and run an AML pipeline every time code is changed in the repo. You will need an Azure Machine Learning workspace available to you.

Hopefully at this point you have forked this repo. After that we will proceed as follows:

1. Add your corresponding environment secrets (see this [json file](../sample_secrets.json) for what is needed) into a single secret called `AMLENV`. 
(**Note**: copy the filled out json file into the secret)
2. Enable the GitHub actions for the repo
3. Make a change to the repo and commit
4. The [build](../.github/workflows/build.yml) workflow should fire.
5. You should see an AML Pipeline start the `prep`, `train`, and `register` process.

