import os

QUEUE_NAME = os.getenv("FBI_QUEUE_NAME", "agent-actions")
DEFAULT_CONNECTION_STRING = os.getenv("FBI_QUEUE_CS", None)
MAX_ITERATIONS = int(os.getenv("FBI_MAX_ITERATIONS", 180))
