from abc import ABC, abstractmethod

#Bot
class ABot(ABC):
    @abstractmethod
    def create_user(self, session_info):
        """Create a user based on session information."""
        pass

    @abstractmethod
    def generate_content(self, sub_session_id, datasets_json, users_id):
        """Generate content based on provided parameters."""
        pass

#Detector
class ADetector(ABC):
    @abstractmethod
    def detect_bot(self, session_data):
        """Detect bot based on the session datasets given."""
        pass