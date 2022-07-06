import pytest
import uuid
import base64
import pdb

from fbi import FbiClient, FbiQueueItem

from conftest import live_only


def create_random_b64_content() -> str:
    content = str(uuid.uuid4()) + str(uuid.uuid4()) + str(uuid.uuid4())

    bytes = content.encode(encoding="utf-8")
    base64_bytes = base64.b64encode(bytes)
    base64_string = base64_bytes.decode("ascii")

    return base64_string


@live_only
def test_send_receive_control_messages(unique_queue_client: FbiClient):
    item = FbiQueueItem(content=create_random_b64_content(), type="control", shell="default")
    unique_queue_client.send_control_message(message=item)
    results = unique_queue_client.peek_control_messages()
    assert len(results) >= 1


@live_only
def test_send_receive_output_messages(unique_queue_client: FbiClient):
    item = FbiQueueItem(content=create_random_b64_content(), type="output", shell="default")
    unique_queue_client.send_output_message(message=item)
    results = unique_queue_client.peek_output_messages()
    assert len(results) >= 1
