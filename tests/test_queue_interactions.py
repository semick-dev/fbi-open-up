import pytest
import uuid
import base64
import pdb

from azure.storage.queue import QueueClient
from fbi.queue_interactions import send_message, get_control_messages, get_output_messages
from fbi import FbiQueueItem


def create_random_b64_content() -> str:
    content = str(uuid.uuid4()) + str(uuid.uuid4()) + str(uuid.uuid4())

    bytes = content.encode(encoding="utf-8")
    base64_bytes = base64.b64encode(bytes)
    base64_string = base64_bytes.decode("ascii")

    return base64_string


@pytest.mark.live_only
def test_send_receive_control_messages(unique_queue_client: QueueClient):
    item = FbiQueueItem(content=create_random_b64_content(), type="control", shell="pwsh")
    send_message(client=unique_queue_client, message=item)
    results = get_control_messages(unique_queue_client)
    assert len(results) >= 1


@pytest.mark.live_only
def test_send_receive_output_messages(unique_queue_client: QueueClient):
    item = FbiQueueItem(content=create_random_b64_content(), type="output", shell="pwsh")
    send_message(client=unique_queue_client, message=item)
    results = get_output_messages(unique_queue_client)
    assert len(results) >= 1
