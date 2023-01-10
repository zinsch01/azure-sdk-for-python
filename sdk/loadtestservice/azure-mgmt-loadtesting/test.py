import json
from azure.identity import DefaultAzureCredential
from azure.mgmt.loadtesting.models import (
    LoadTestResourcePatchRequestBody,
    EncryptionProperties,
    EncryptionPropertiesIdentity,
)
from azure.mgmt.loadtesting import LoadTestMgmtClient

body = LoadTestResourcePatchRequestBody(
    encryption=EncryptionProperties(
        identity=EncryptionPropertiesIdentity(type="SystemAssigned", resource_id=None),
        key_url="xxx",
    )
)

# The serialized result doesn't have null
client = LoadTestMgmtClient(DefaultAzureCredential(), "sub_id")
result1 = client._serialize.body(body, "LoadTestResourcePatchRequestBody")
print("result1:")
print(result1)


# The serialized result doesn't have null
body = {'properties': {'encryption': {'identity': {'type': 'SystemAssigned', 'resourceId': None}, 'keyUrl': 'xxx'}}}
result2 = json.dumps(body)
print("result2:")
print(result2)
