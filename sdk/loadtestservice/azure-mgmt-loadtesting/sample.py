import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.mgmt.loadtesting.models import (
    LoadTestResourcePatchRequestBody,
    EncryptionProperties,
    EncryptionPropertiesIdentity,
)
from azure.mgmt.loadtesting import LoadTestMgmtClient

load_dotenv()
client = LoadTestMgmtClient(
    credential=DefaultAzureCredential(),
    subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID", "000"),
)

body = LoadTestResourcePatchRequestBody(
    encryption=EncryptionProperties(
        identity=EncryptionPropertiesIdentity(type="SystemAssigned"),
        key_url="xxx",
    )
)

# set None manually
def customize_body(request_body):
    request_body["properties"]["encryption"]["identity"].update({"resourceId": None})

result = client.load_tests.begin_update(
    resource_group_name="groupName",
    load_test_name="testName",
    load_test_resource_patch_request_body=body,
    customize_body=customize_body
).result()
print(result.serialize())