import json

class ErrorMessage:
    def __init__(self,return_code, error_message):
        self.return_code = return_code
        self.error_message = error_message
    
    def to_json(self):
        return json.dumps({"status": self.return_code, "data":{"error_message":self.error_message}})