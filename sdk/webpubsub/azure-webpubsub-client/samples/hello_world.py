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
import openai

load_dotenv()

def main():
    service_client = WebPubSubServiceClient.from_connection_string(
        connection_string=os.getenv("WEBPUBSUB_CONNECTION_STRING"), hub="hub"
    )
    url = service_client.get_client_access_token(roles=["webpubsub.joinLeaveGroup", "webpubsub.sendToGroup"])["url"]
    print(url)

    client = WebPubSubClient(credential=url, options=WebPubSubClientOptions(auto_reconnect=False))

    client.start()
    group_name = "test"
    openai.api_type = "azure"
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_base = os.getenv("OPENAI_API_BASE")
    openai.api_version = "2022-12-01"
    conversation = ["Marv is a chatbot that reluctantly answers questions."]

    def on_connected(msg: OnConnectedArgs):
        print("======== connected ===========")
        print(f"Connection {msg.connection_id} is connected")


    def on_disconnected(msg: OnDisconnectedArgs):
        print("========== disconnected =========")
        print(f"connection is disconnected: {msg.message}")


    def on_group_message(msg: OnGroupDataMessageArgs):
        print("========== group message =========")
        print(f"Received message from {msg.message.group}: {msg.message.data}")
        conversation.append("Human: " + msg.message.data)
        result = openai.Completion.create(engine="text-davinci-003", prompt=" ".join(conversation), max_token="256")
        if len(result.choices) > 1:
            raise Exception("exception")
        print(result.choices[0].text)
        conversation.append(result.choices[0].text)
        client.send_to_group(group_name, result.choices[0].text, "text", SendToGroupOptions(no_echo=True, fire_and_forget=True))

    client.on("connected", on_connected)
    client.on("disconnected", on_disconnected)
    client.on("group-message", on_group_message)

    client.join_group(group_name)
    time.sleep(600)    
    client.stop()

if __name__ == "__main__":
    main()
