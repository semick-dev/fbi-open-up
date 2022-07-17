import argparse
import os
import pdb
import time
import subprocess
import platform

from azure.storage.queue import QueueClient

from fbi.FbiQueueItem import FbiQueueItem

from ..LocalInvocationClient import LocalInvocationClient

from ..config import QUEUE_NAME, DEFAULT_CONNECTION_STRING, MAX_ITERATIONS
from ..FbiClient import FbiClient


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
    invocation_client = LocalInvocationClient(os.getcwd())
    iteration = 1

    print("Connected to {}.".format(client.control_client.account_name + " -> " + client.control_client.queue_name))

    client.send_output_message(
        FbiQueueItem(
            content="Hello from {}".format(platform.node()),
            additional_data=platform.node(),
            type="startup",
            cwd=invocation_client.cwd,
        )
    )

    while True and iteration <= MAX_ITERATIONS:
        if args.verbose:
            print("Iteration {}".format(iteration))

        control_msg = client.get_control_message()

        if control_msg is not None:
            if args.verbose:
                print(control_msg)

            output = invocation_client.run(control_msg)
            client.send_output_message(output)
            print(output.content)

        time.sleep(1)
        iteration += 1
