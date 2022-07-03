import os

QUEUE_NAME = os.getenv("FBI_QUEUE_NAME", "fbi")
DEFAULT_CONNECTION_STRING = os.getenv("FBI_QUEUE_CS", None)
