import argparse
import os
import pdb
import time

from ..FbiClient import FbiClient
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

    iteration = 0

    client = FbiClient(cs, QUEUE_NAME)

    print("Connected to {}.".format())

    while True:
        output_msg = client.get_output_message()

        if output_msg is not None:
            if args.verbose:
                print(output_msg)

        iteration += 1
        time.sleep(1)
