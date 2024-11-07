from abc_classes import ADetector
from teams_classes import DetectionMark

class Detector(ADetector):
    def detect_bot(self, session_data):
        # todo logic
        # Example:
        marked_account = []
        
        for user in session_data.users:
            marked_account.append(DetectionMark(user_id=user['id'], confidence=50, bot=False))

        return marked_account
    