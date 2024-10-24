from abc_classes import ADetector
from teams_classes import DetectionMark

class Detector(ADetector):
    def detect_bot(self, session_data):
        # todo logic
        # Example:
        marked_account = [
            DetectionMark(user_id='5fbc46b0-2a80-4dc5-b499-fae4bdb335c1', confidence=90, bot=True),
            DetectionMark(user_id='976978627425312768', confidence=100, bot=True),
            DetectionMark(user_id='787467017406251008', confidence=100, bot=False)
        ]

        return marked_account
    