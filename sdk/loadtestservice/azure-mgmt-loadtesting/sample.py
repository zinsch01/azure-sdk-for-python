import json
import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.loadtesting.models import (
    LoadTestResourcePatchRequestBody,
    EncryptionProperties,
    EncryptionPropertiesIdentity,
)
from azure.mgmt.loadtesting import LoadTestMgmtClient

client = LoadTestMgmtClient(
    credential=DefaultAzureCredential(),
    subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID", "000"),
)

origin_body = LoadTestResourcePatchRequestBody(
    encryption=EncryptionProperties(
        identity=EncryptionPropertiesIdentity(type="SystemAssigned", resource_id=None),
        key_url="xxx",
    )
)

# get serialized body
serialized_body = origin_body.serialize()
print(serialized_body)

# set None manually
serialized_body["properties"]["encryption"]["identity"].update({"resourceId": None})
body = json.dumps(serialized_body)
print(body)

result = client.load_tests.begin_update(
    resource_group_name="groupName",
    load_test_name="testName",
    load_test_resource_patch_request_body=body
).result()
print(result.serialize())