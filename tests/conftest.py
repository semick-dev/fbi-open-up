import pytest
import os
import uuid
import pdb
from azure.storage.queue import QueueClient

from dotenv import load_dotenv
from fbi import FbiClient

load_dotenv()

COMMON_QUEUE_NAME = "test"

def pytest_addoption(parser):
    parser.addoption('--live_only', action='store_true', dest="live_only",
                 default=False, help="Enable Live Tests")

live_only = pytest.mark.skipif("not config.getoption('live_only')")

def get_queue_client(queue_name: str) -> FbiClient:
    cs = os.getenv("TEST_ACCOUNT_CONNECTION_STRING")
    client = FbiClient(cs, base_queue_name=queue_name)

    client.create_queues()

    return client


@pytest.fixture
def unique_queue_client() -> FbiClient:
    client = get_queue_client(COMMON_QUEUE_NAME + str(uuid.uuid4()).lower())

    yield client

    client.delete_queues()


@pytest.fixture
def common_queue_client() -> QueueClient:
    client = get_queue_client(COMMON_QUEUE_NAME)

    yield client

    client.delete_queues()
