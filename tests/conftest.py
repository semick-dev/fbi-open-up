import pytest
import os
import uuid
import pdb
from azure.storage.queue import QueueClient

from dotenv import load_dotenv

load_dotenv()

COMMON_QUEUE_NAME = "test"


def get_queue_client(queue_name: str) -> QueueClient:
    cs = os.getenv("TEST_ACCOUNT_CONNECTION_STRING")
    client = QueueClient.from_connection_string(cs, queue_name=queue_name)

    # cbf to search the documentation to find queue status, exception for now
    try:
        client.delete_queue()
    except:
        pass

    client.create_queue()

    return client


@pytest.fixture
def unique_queue_client() -> QueueClient:
    client = get_queue_client(COMMON_QUEUE_NAME + str(uuid.uuid4()))

    yield client

    client.delete_queue()


@pytest.fixture
def common_queue_client() -> QueueClient:
    client = get_queue_client(COMMON_QUEUE_NAME)

    yield client

    client.delete_queue()
