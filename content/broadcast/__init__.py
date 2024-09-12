from abc import ABC, abstractmethod


class SMSClient(ABC):
    @abstractmethod
    async def send_message(self, recipients: list[dict]) -> bool:
        """Sends SMS messages asynchronously."""
        pass
