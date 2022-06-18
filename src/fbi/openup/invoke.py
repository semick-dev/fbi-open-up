import argparse
import os
import pdb
import time

from azure.storage.queue import QueueClient

from ..FbiQueueItem import FbiQueueItem
from ..queue_interactions import get_output_messages
from ..config import QUEUE_NAME, DEFAULT_CONNECTION_STRING

def main():
    parser = argparse.ArgumentParser(
        description="This CLI app is used on a user's machine, and is used to interact with the remote devops agent."
    )

    parser.add_argument(
        "-c",
        "--connectionstring",
        dest="cs",
        help="The blob storage connection string. If not provided, will fall back to FBI_CONNECTION_STRING.",
    )
    args = parser.parse_args()

    cs = args.cs
    if not args.cs:
        if not DEFAULT_CONNECTION_STRING:
            raise "Need a valid connection string to run"
        cs = DEFAULT_CONNECTION_STRING
    
    client = QueueClient.from_connection_string(cs, QUEUE_NAME)

    try:
        client.delete_queue()
    except:
        pass

    client.create_queue

    while True:
        time.sleep(1)