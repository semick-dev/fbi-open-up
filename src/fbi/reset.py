import argparse
from fbi.config import QUEUE_NAME, DEFAULT_CONNECTION_STRING, MAX_ITERATIONS
from fbi import LocalInvocationClient, FbiClient


def reset():
    parser = argparse.ArgumentParser(
        description="This CLI app is used on a user's machine, and is used to blow away the control and output queues in case of bad state."
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

    print(
        "Connected to {}.".format(
            client.output_client.account_name
            + " "
            + client.control_client.queue_name
            + "/"
            + client.output_client.queue_name
        )
    )
    client.delete_queues()
    client.create_queues()
