import json
import base64


class FbiQueueItem:
    def __init__(self, content: str, type: str, shell: str, cwd: str = None) -> None:
        # b64 encoded raw shell output from agent
        self.content = content
        # type of message. "control" or "output"
        self.type = type
        # what shell was the command invoked on?
        self.shell = shell
        # only populated in output message, what is the current working directory?
        self.cwd = cwd

    @classmethod
    def load_from_json_string(cls, json_content: str):
        doc = json.loads(json_content)

        cwd = None
        if doc["cwd"]:
            cwd = doc["cwd"]

        return cls(content=doc["content"], type=doc["type"], shell=doc["shell"], cwd=cwd)

    def decode_content(self, input_str: str):
        b64_encoded_bytes = input_str.encode("utf-8")
        original_bytes = base64.b64decode(b64_encoded_bytes)
        original_string = original_bytes.decode("utf-8")
        return original_string

    def encode_content(self, input_str: str):
        input_str_bytes = input_str.encode("utf-8")
        base64_bytes = base64.b64encode(input_str_bytes)
        base64_string = base64_bytes.decode("utf-8")
        return base64_string

    # returns a base64 encoded content string
    def as_json(self) -> str:
        raw_json = json.dumps(self.__dict__)
        return raw_json
