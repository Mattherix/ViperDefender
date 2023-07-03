from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient

credential = AzureCliCredential()

subscription_id = "b316987e-9c71-46d5-a608-610b9bc8234d"

resource_client = ResourceManagementClient(credential, subscription_id)

# Provision the resource group.
rg_result = resource_client.resource_groups.create_or_update(
    "PythonAzureExample-rg", {"location": "francecentral"}
)

print(
    f"Provisioned resource group {rg_result.name} in \
        the {rg_result.location} region"
)

rg_result = resource_client.resource_groups.create_or_update(
    "PythonAzureExample-rg",
    {
        "location": "francecentral",
        "tags": {"environment": "test", "department": "tech"},
    },
)

print(f"Updated resource group {rg_result.name} with tags")

# Optional lines to delete the resource group. begin_delete is asynchronous.
poller = resource_client.resource_groups.begin_delete(rg_result.name)
result = poller.result()