import os
import pdb
import platform

from ctypes import ArgumentError
from typing import List
from azure.storage.queue import QueueClient, QueueMessage

from .FbiQueueItem import FbiQueueItem


class FbiClient:
    def __init__(self, connection_string: str, base_queue_name: str, autocreate: bool = True):
        if connection_string == "" or base_queue_name == "":
            raise ArgumentError("One must provide a fully populated queue_name/connection string pair.")

        self.base_queue_name: str = base_queue_name
        self.control_queue_name: str = "{}-control".format(base_queue_name)
        self.output_queue_name: str = "{}-output".format(base_queue_name)

        self.control_client: QueueClient = QueueClient.from_connection_string(
            connection_string, self.control_queue_name
        )
        self.output_client: QueueClient = QueueClient.from_connection_string(connection_string, self.output_queue_name)

        if autocreate:
            self.create_queues()

    def get_message(self, client: QueueClient) -> FbiQueueItem:
        msg = client.receive_message()

        if msg is not None:
            client.delete_message(msg)
            return FbiQueueItem.load_from_json_string(msg.content)

        return None

    def send_message(self, client: QueueClient, message: FbiQueueItem) -> QueueMessage:
        try:
            result = client.send_message(content=message.as_json())
        except BaseException as e:
            raise

        return result

    def send_control_message(self, message: FbiQueueItem) -> None:
        self.send_message(self.control_client, message)

    def get_control_message(self) -> FbiQueueItem:
        return self.get_message(self.control_client)

    def send_output_message(self, message: FbiQueueItem) -> None:
        self.send_message(self.output_client, message)

    def get_output_message(self) -> FbiQueueItem:
        return self.get_message(self.output_client)

    def create_queues(self, include_control: bool = True, include_output: bool = True):
        if include_control:
            try:
                self.control_client.create_queue()
            except Exception as e:
                # todo: specific logic here
                pass

        if include_output:
            try:
                self.output_client.create_queue()
            except Exception as e:
                # todo: specific logic here
                pass

    def clear_queues(self, include_control: bool = True, include_output: bool = True):
        if include_control:
            try:
                self.control_client.clear_messages()
            except Exception as e:
                # todo: specific logic here
                pass

        if include_output:
            try:
                self.output_client.clear_messages()
            except Exception as e:
                # todo: specific logic here
                pass

    def delete_queues(self, include_control: bool = True, include_output: bool = True):
        if include_control:
            try:
                self.control_client.delete_queue()
            except Exception as e:
                # todo: specific logic here
                pass

        if include_output:
            try:
                self.output_client.delete_queue()
            except Exception as e:
                # todo: specific logic here
                pass

    def peek_control_messages(self) -> List[FbiQueueItem]:
        messages = self.control_client.peek_messages()
        return [FbiQueueItem.load_from_json_string(msg.content) for msg in messages]

    def peek_output_messages(self) -> List[FbiQueueItem]:
        messages = self.output_client.peek_messages()
        return [FbiQueueItem.load_from_json_string(msg.content) for msg in messages]
