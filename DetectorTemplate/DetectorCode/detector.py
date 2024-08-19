from abc import ABC, abstractmethod
from teams_classes import DetectionMark

class ADetector(ABC):
    @abstractmethod
    def detect_bot(self, session_data):
        """Detect bot based on the session datasets given."""
        pass

class Detector(ADetector):
    def detect_bot(self, session_data):
        # todo logic
        marked_account = [
            DetectionMark(userId='8d925460-8b23-4f12-a07e-2541891c7ef1', confidence=90, bot=True),
            DetectionMark(userId='6e28897d-77db-4292-a3b4-c4f35fe55f7f', confidence=100, bot=True)
        ]

        return marked_account
    