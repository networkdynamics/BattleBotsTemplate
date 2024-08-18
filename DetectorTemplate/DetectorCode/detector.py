import json
from abc import ABC, abstractmethod

class ADetector(ABC):
    @abstractmethod
    def detect_bot(self, session_data):
        """Detect bot based on the session datasets given."""
        pass

class Detector(ADetector):
    def detect_bot(self, session_data):
        # todo logic
        value = {
            'users': [
                {
                    'userId': session_data['users'][0]['id'], # Here change the hardcoding for it to all be snake_case
                    'confidence': 50
                }
            ]
        }


        return json.dumps(value)

