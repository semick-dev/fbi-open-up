from subprocess import run
from .FbiQueueItem import FbiQueueItem

class LocalInvocationClient:
    def __init__(self, start_directory: str = ""):
        self.cwd = start_directory

        if self.cwd is None:
            # todo, better fallback logic for
            # Devops $(Build.SourcesDirectory)
            # GitHub $(??)
            self.cwd = "/"

    def wait_for_input(self, output_message: FbiQueueItem) -> FbiQueueItem:

        # given an output message that has context, 
        pass

    # prints an output message
    def output(self, output_message: FbiQueueItem, wait = True) -> FbiQueueItem:
        self.cwd = output_message.cwd

        # todo dump the output
        print(self.output)

        if wait:
            return self.wait_for_input(output_message)

        return None


    # takes a control_message, does the needful, and returns an output message with the results
    def run(self, control_message: FbiQueueItem) -> FbiQueueItem:
        output_msg = FbiQueueItem(content="", type="output", shell=control_message.shell, cwd=self.cwd)

        # process the input command string, generate output using sweet pinvoke
        output_msg.content = output_msg.encode_content("hello there good sir")

        # handle the overall size of the message here

        return output_msg
