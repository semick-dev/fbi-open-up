from ctypes import ArgumentError
from .FbiQueueItem import FbiQueueItem
from azure.storage.queue import QueueClient, QueueMessage
import os
import pdb
from typing import List

# todo, convert to doccomennted KWARGS
def send_message(message: FbiQueueItem, client: QueueClient = None, cs: str = "", queue_name: str = "") -> None:
    if client is None and cs == "" and queue_name == "":
        raise ArgumentError(
            "One must provide a fully populated queue_name/connection string pair, OR provide a valid QueueClient"
        )

    if client is None:
        client = QueueClient.from_connection_string(cs, queue_name)

    try:
        result = client.send_message(content=message.asJson())
    except BaseException as e:
        raise


def filter_msg_list(messages: List[QueueMessage], type: str) -> List[FbiQueueItem]:
    items = [FbiQueueItem.load_from_json_string(msg.content) for msg in messages]
    return [msg for msg in items if msg.type == type]


def get_message(client: QueueClient = None, cs: str = "", queue_name: str = "") -> FbiQueueItem:
    if client is None and cs == "" and queue_name == "":
        raise ArgumentError(
            "One must provide a fully populated queue_name/connection string pair, OR provide a valid QueueClient"
        )

    if client is None:
        client = QueueClient.from_connection_string(cs, queue_name)

    msg = client.receive_message()
    client.delete_message(msg)

    return FbiQueueItem.load_from_json_string(msg.content)
    


def get_control_messages(client: QueueClient = None, cs: str = "", queue_name: str = "") -> FbiQueueItem:
    if client is None and cs == "" and queue_name == "":
        raise ArgumentError(
            "One must provide a fully populated queue_name/connection string pair, OR provide a valid QueueClient"
        )

    if client is None:
        client = QueueClient.from_connection_string(cs, queue_name)

    messages = client.peek_messages()
    return filter_msg_list(messages, "control")


def get_output_message(client: QueueClient = None, cs: str = "", queue_name: str = "") -> FbiQueueItem:
    if client is None and cs == "" and queue_name == "":
        raise ArgumentError(
            "One must provide a fully populated queue_name/connection string pair, OR provide a valid QueueClient"
        )

    if client is None:
        client = QueueClient.from_connection_string(cs, queue_name)

    messages = client.peek_messages()
    return filter_msg_list(messages, "output")
