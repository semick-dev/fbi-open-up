import argparse
import pdb
from ..QueueItem import QueueItem
from ..queue_interactions import get_output_message

def main():
    parser = argparse.ArgumentParser(
        description="This CLI app is used on a user's machine, and is used to interact with the remote devops agent."
    )

    parser.add_argument(
        "-c",
        "--connectionstring",
        dest="cs",
        help="The blob storage connection string. If not provided, will fall back to FBI_CONNECTION_STRING."
    )
    args = parser.parse_args()
    

    print("hello world")