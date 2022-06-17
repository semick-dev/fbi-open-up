import base64
import json

class QueueItem:
    def __init__(self, content: str, type: str, shell: str) -> None:
        self.content = content
        self.type = type
        self.shell = shell

    @classmethod
    def load_from_json_string(cls, base64_json_content: str):
        raw_json = base64.b64decode(base64_json_content)
        doc = json.loads(raw_json)
        return cls(content=doc["content"], type=doc["type"], shell=doc["shell"])

    # returns a base64 encoded content string
    def asJson(self) -> str:
        raw_json = json.dumps(self.__dict__)
        encoded_json = base64.encode(raw_json)
        return encoded_json.decode('ascii')


