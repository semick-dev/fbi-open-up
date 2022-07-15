import json
import base64
import pdb


class FbiQueueItem:
    def __init__(
        self, content: str, type: str = None, shell: str = None, cwd: str = None, additional_data: str = None
    ) -> None:
        # content is encoded for easy upload / json-ing later
        self._content = self.encode_content(content)
        # type of message. "control" or "output"
        self.type = type
        # what shell was the command invoked on?
        self.shell = shell
        # only populated in output message, what is the current working directory?
        self.cwd = cwd

        self.additional_data = additional_data

    @property
    def content(self) -> str:
        if self._content:
            return self.decode_content(self._content)
        else:
            return self._content

    @content.setter
    def content(self, setting: str) -> None:
        self._content = self.encode_content(setting)

    @classmethod
    def load_from_json_string(cls, json_content: str):
        doc = json.loads(json_content)

        return cls(
            content=doc["_content"],
            type=doc["type"],
            shell=doc["shell"],
            cwd=doc["cwd"],
            additional_data=doc["additional_data"],
        )

    def decode_content(self, input_str: str):
        b64_encoded_bytes = input_str.encode("utf-8")
        original_bytes = base64.b64decode(b64_encoded_bytes)
        original_string = original_bytes.decode("utf-8")

        # todo, why do I need to double decode? as far as I can tell I'm not double encoding
        b64_encoded_bytes = original_string.encode("utf-8")
        original_bytes = base64.b64decode(b64_encoded_bytes)
        original_string = original_bytes.decode("utf-8")

        return original_string.encode("latin-1", "backslashreplace").decode("unicode-escape")

    def encode_content(self, input_str: str):
        input_str_bytes = input_str.encode("utf-8")
        base64_bytes = base64.b64encode(input_str_bytes)
        base64_string = base64_bytes.decode("utf-8")
        return base64_string

    # returns a base64 encoded content string
    def as_json(self) -> str:
        raw_json = json.dumps(self.__dict__)
        return raw_json
