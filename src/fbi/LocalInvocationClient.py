import subprocess
import tempfile
import os
import uuid
import platform
import pdb

from subprocess import run as process_run
from typing import List
from .FbiQueueItem import FbiQueueItem


class LocalInvocationClient:
    def __init__(self, start_directory: str = ""):
        self.cwd = start_directory

        current_plat = platform.system()
        if current_plat == "Windows":
            self.invocation_command = ["pwsh", "-c"]
        else:
            self.invocation_command = ["bash", "-c"]

        if self.cwd is None:
            # todo, better fallback logic for
            # Devops $(Build.SourcesDirectory)
            # GitHub $(??)
            self.cwd = "/"

    def wait_for_input(self, output_message: FbiQueueItem) -> FbiQueueItem:
        content = input("[remote connection] {}> ".format(output_message.cwd))

        return FbiQueueItem(content, cwd=self.cwd)

    # prints an output message
    def output(self, output_message: FbiQueueItem, wait=True) -> FbiQueueItem:
        self.cwd = output_message.cwd

        # todo dump the output
        print(output_message.content)

        if wait:
            return self.wait_for_input(output_message)

        return None

    def get_command(self, control_message: FbiQueueItem) -> str:
        if control_message.content.lower().startswith("cd"):
            # parse cd, change working directory

            return None
        else:
            # return control_message.content
            return control_message.content

    def get_temp_file(self) -> str:
        tmpfile = tempfile.mkstemp(suffix=".txt")
        os.close(tmpfile[0])
        return tmpfile[1]

    def cleanup_temp_file(self, temp_file: str) -> None:
        os.remove(temp_file)

    # checks a temp_file that contains command output. if it is too large to fit in a queue message, upload it
    # and return a reference to that uploaded blob as "reference::<blobpath>", otherwise just returns the file contents
    # as a string
    def prepare_message_content(self, temp_file: str) -> str:
        if os.path.getsize(temp_file) >= 61440:
            blob_name = uuid.uuid4()

            # logic to upload the file to blob storage and get that resulting uuid
            return "reference::<blobpath>"
        else:
            with open(temp_file, "r", encoding="utf-8") as f:
                text = f.read()
            return text

    # takes a control_message, does the needful, and returns an output message with the results
    def run(self, control_message: FbiQueueItem) -> FbiQueueItem:
        output_msg = FbiQueueItem(content="", type="output", shell=control_message.shell, cwd=self.cwd)

        command = self.get_command(control_message)

        try:
            if command is not None:
                temp_file = self.get_temp_file()
                with open(temp_file, "w", encoding="utf-8") as f:
                    process_run(
                        self.invocation_command + [command],
                        cwd=self.cwd,
                        shell=True,
                        stdout=f,
                        stderr=subprocess.STDOUT,
                    )
                content = self.prepare_message_content(temp_file)
                output_msg.content = content

            # change directory
            elif command is None:
                output_msg.cwd = self.cwd
            else:
                print("No idea how we got here.")
        except Exception as e:
            output_msg.content = str(e)
        finally:
            self.cleanup_temp_file(temp_file)

        return output_msg
