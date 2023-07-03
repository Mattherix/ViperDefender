# orchestrator

To install all the dev tools follow this [tutorial](https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python?pivots=python-mode-decorators)

Create a local.settings.json file:

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "VIRUSTOTAL_API_KEY": "{{ Your virustotal key -> https://support.virustotal.com/hc/en-us/articles/115002100149-API }}",
    "MONGO_URI": "{{ your cosmosdb uri -> https://learn.microsoft.com/en-us/rest/api/cosmos-db/cosmosdb-resource-uri-syntax-for-rest }}"
  }
}
```