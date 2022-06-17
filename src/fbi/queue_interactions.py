from . import QueueItem
from azure.storage.queue import QueueClient
import os
import pdb

def get_control_message(cs: str, queue_name: str) -> QueueItem:
    queue_client = QueueClient.from_connection_string(cs, queue_name)

    messages = queue_client.peek_messages()

    for peeked_message in messages:
        print("Peeked message: " + peeked_message.content)
    pdb.set_trace()
    pass

def get_output_message(cs: str, queue_name: str) -> QueueItem:
    queue_client = QueueClient.from_connection_string(cs, queue_name)
    
    messages = queue_client.peek_messages()

    for peeked_message in messages:
        print("Peeked message: " + peeked_message.content)
    
    
    