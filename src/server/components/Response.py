import json

class Response:
    def __init__(self, return_code, type, **kwargs):
        self.return_code = return_code
        self.type = type
        self.data = {"type": type}
        self.data.update(kwargs)

    def to_json(self):
        return json.dumps({"status": self.return_code, "data": self.data})