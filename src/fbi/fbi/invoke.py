import argparse
import pdb
from ..QueueItem import QueueItem
from ..queue_interactions import get_control_message

def main():
    parser = argparse.ArgumentParser(
        description="This CLI app is used on a devops or actions agent to respond to debugging messages."
    )

    parser.add_argument(
        "-c",
        "--connectionstring",
        dest="cs",
        help="The blob storage connection string. If not provided, will fall back to FBI_CONNECTION_STRING."
    )
    args = parser.parse_args()
    
    