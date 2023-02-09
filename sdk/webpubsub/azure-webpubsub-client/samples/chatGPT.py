import os
import time
from azure.webpubsub.client import WebPubSubClient
from azure.messaging.webpubsubservice import WebPubSubServiceClient
from azure.webpubsub.client import (
    OnConnectedArgs,
    SendToGroupOptions,
    WebPubSubClientOptions,
    OnGroupDataMessageArgs,
    OnDisconnectedArgs,
)
from dotenv import load_dotenv

load_dotenv()

def on_group_message(msg: OnGroupDataMessageArgs):
    print("->" + msg.message.data)


service_client = WebPubSubServiceClient.from_connection_string(
    connection_string=os.getenv("WEBPUBSUB_CONNECTION_STRING"), hub="hub"
)
url = service_client.get_client_access_token(roles=["webpubsub.joinLeaveGroup", "webpubsub.sendToGroup"])["url"]
client = WebPubSubClient(credential=url, options=WebPubSubClientOptions(auto_reconnect=False))
client.on("group-message", on_group_message)

client.start()
group_name = "test"
client.join_group(group_name)
while True:
    question = input()
    if not question:
        break
    client.send_to_group(group_name, question, "text", SendToGroupOptions(no_echo=True, fire_and_forget=True))
client.stop()