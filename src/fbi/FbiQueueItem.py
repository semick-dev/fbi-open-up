import json


class FbiQueueItem:
    def __init__(self, content: str, type: str, shell: str) -> None:
        # b64 encoded raw shell output from agent
        self.content = content
        # type of message. "control" or "output"
        self.type = type
        # what shell was the command invoked on?
        self.shell = shell

    @classmethod
    def load_from_json_string(cls, json_content: str):
        doc = json.loads(json_content)
        return cls(content=doc["content"], type=doc["type"], shell=doc["shell"])

    # returns a base64 encoded content string
    def asJson(self) -> str:
        raw_json = json.dumps(self.__dict__)
        return raw_json
