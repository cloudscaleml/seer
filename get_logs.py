from azureml.core import Workspace

ws = Workspace.from_config()
print(ws.webservices['seer-deployment'].get_logs())