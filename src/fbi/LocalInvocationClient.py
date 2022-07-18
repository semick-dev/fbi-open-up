import subprocess
import tempfile
import os
import uuid
import platform
import pdb
import shlex

from colorama import Fore, Style
from subprocess import run as process_run
from typing import List, Tuple
from .FbiQueueItem import FbiQueueItem


class LocalInvocationClient:
    def __init__(self, start_directory: str = None):
        self.cwd = start_directory

        self.remote_agent_name = "devops agent"

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
        content = input(
            Fore.GREEN + "[{}]".format(self.remote_agent_name) + Style.RESET_ALL + " {}>".format(output_message.cwd)
        )

        return FbiQueueItem(content=content, cwd=self.cwd)

    def write_output(self, message: FbiQueueItem) -> None:
        print(message.content)

    # prints an output message
    def output(self, output_message: FbiQueueItem, wait=True) -> FbiQueueItem:
        self.cwd = output_message.cwd

        self.write_output(output_message)

        if wait:
            return self.wait_for_input(output_message)

        return None

    def parse_cd(self, command_string: str) -> str:
        pass

    def get_command(self, control_message: FbiQueueItem) -> Tuple[str, str]:
        if control_message.content.lower().startswith("cd"):
            target = control_message.content[2:].lstrip()
            # cd <relative path>
            # we just ignore the first few characters and let change directory figure out what we mean.
            # otherwise we would do ltrim.
            try:
                os.chdir(target)
            except Exception as e:
                pdb.set_trace()
                raise Exception('Unable to change directory to "{}"'.format(target))

            self.cwd = os.getcwd()

            return (None, None)
        else:
            return (control_message.content, None)

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
        cleanup = False
        try:
            command, command_error = self.get_command(control_message)

            if command is not None:
                cleanup = True
                temp_file = self.get_temp_file()
                with open(temp_file, "w", encoding="utf-8") as f:
                    invocation = []

                    if platform.system() == "Windows":
                        invocation = self.invocation_command + [command]
                    else:
                        invocation = self.invocation_command + ['"{}"'.format(shlex.quote(command))]
                    process_run(
                        invocation,
                        cwd=self.cwd,
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
            if cleanup:
                self.cleanup_temp_file(temp_file)

        return output_msg
