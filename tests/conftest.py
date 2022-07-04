import pytest
import os
import uuid
import pdb
from azure.storage.queue import QueueClient

from dotenv import load_dotenv
from fbi import FbiClient, LocalInvocationClient

load_dotenv()

COMMON_QUEUE_NAME = "test"
root_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", ".."))
live_only = pytest.mark.skipif("not config.getoption('live_only')")


def pytest_addoption(parser):
    parser.addoption("--live_only", action="store_true", dest="live_only", default=False, help="Enable Live Tests")


def get_queue_client(queue_name: str) -> FbiClient:
    cs = os.getenv("TEST_ACCOUNT_CONNECTION_STRING")
    client = FbiClient(cs, base_queue_name=queue_name)

    client.create_queues()

    return client


@pytest.fixture
def local_client() -> LocalInvocationClient:
    client = LocalInvocationClient(root_dir)

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
