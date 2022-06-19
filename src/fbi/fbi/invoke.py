import argparse
import os
import pdb
import time

from azure.storage.queue import QueueClient

from ..config import QUEUE_NAME, DEFAULT_CONNECTION_STRING
from ..FbiQueueItem import FbiQueueItem
from ..queue_interactions import get_control_messages

# takes an input control command, generates an output message
def run_command(control_message: FbiQueueItem) -> FbiQueueItem:
    output_msg = FbiQueueItem(content="", type="output", shell=control_message.shell)

    # process the input command string, gemerate output using sweet pinvoke
    return output_msg

def main():
    parser = argparse.ArgumentParser(
        description="This CLI app is used on a devops or actions agent to respond to debugging messages."
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
    
    control_client = QueueClient.from_connection_string(cs, QUEUE_NAME + "control")
    output_client = QueueClient.from_connection_string(cs, QUEUE_NAME + "output")

    while True:
        time.sleep(1)
