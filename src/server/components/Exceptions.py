import json

class Exceptions:
    def __init__(self,error_code, error_message):
        self.error_code = error_code
        self.error_message = error_message
    
    def to_json(self):
        return json.dumps({"status": self.error_code, "data":{"error_message":self.error_message}})