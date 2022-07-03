import argparse
import os
import pdb
import time
import subprocess

from azure.storage.queue import QueueClient

from ..LocalInvocationClient import LocalInvocationClient

from ..config import QUEUE_NAME, DEFAULT_CONNECTION_STRING
from ..FbiQueueItem import FbiQueueItem
from ..FbiClient import FbiClient

# takes an input control command, generates an output message
def run_command(control_message: FbiQueueItem) -> FbiQueueItem:
    output_msg = FbiQueueItem(content="", type="output", shell=control_message.shell)

    # process the input command string, gemerate output using sweet pinvoke
    output_msg.content = output_msg.encode_content("hello there good sir")

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

    parser.add_argument(
        "-v" "--verbose",
        dest="verbose",
        action="store_true",
        help="Verbosity setting.",
    )
    args = parser.parse_args()

    cs = args.cs
    if not args.cs:
        if not DEFAULT_CONNECTION_STRING:
            raise "Need a valid connection string to run"
        cs = DEFAULT_CONNECTION_STRING

    client = FbiClient(cs, QUEUE_NAME)
    invocation_client = LocalInvocationClient()

    print("Connected to {}.".format())

    while True:
        if args.verbose:
            print("Iteration {}".format(iteration))

        control_msg = client.get_control_message()

        if control_msg is not None:
            if args.verbose:
                print(control_msg)

            output = invocation_client.run(control_msg)
            client.send_output_message(output)

        time.sleep(1)
        iteration += 1
