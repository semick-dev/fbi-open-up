# unique_queue_client and common_queue_client fixtures are available from conftest
import pdb
import pytest
from conftest import live_only, local_client, windows_only
from fbi import FbiQueueItem, LocalInvocationClient

# on test signature add mocker
# def test_func(mocker):
#     mocker.patch(
#         'fbi.FbiClient.get_message',
#         mock_control_item
#     )


def test_valid_control_message_1(local_client: LocalInvocationClient):
    mock_control_item = FbiQueueItem(content="ls")
    result = local_client.run(mock_control_item)
    assert result is not None

    decoded_content = result.content
    assert "dev_requirements.txt" in decoded_content


@windows_only
def test_valid_control_message_2(local_client: LocalInvocationClient):
    mock_control_item = FbiQueueItem(content="gci")
    result = local_client.run(mock_control_item)
    assert result is not None


def test_valid_control_message_3(local_client: LocalInvocationClient):
    mock_control_item = FbiQueueItem(content="ls")
    result = local_client.run(mock_control_item)
    assert result is not None

    decoded_content = result.content
    print(decoded_content)
    assert "dev_requirements.txt" in decoded_content
