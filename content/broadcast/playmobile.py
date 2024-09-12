import aiohttp
import time
from uuid import uuid4
from typing import Optional
from fastapi import Depends
from core import settings
from db.redis import get_redis_client, ICasheClient
from . import SMSClient
import json


class BrokerClient(SMSClient):
    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,
        originator: str,
        redis_client: ICasheClient,
        auth_ttl: int = 300,
        message_ttl: int = 300
    ):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.originator = originator
        self.auth_ttl = auth_ttl
        self.message_ttl = message_ttl
        self.redis_client = redis_client
        self.redis_key = "playmobile:auth"

    async def get_auth(self) -> aiohttp.BasicAuth:
        """Provides a cached or new authentication header using the custom Redis client."""
        return aiohttp.BasicAuth(login=self.username, password=self.password)

    async def refresh_auth(self):
        """Refreshes the cached auth header and updates the custom Redis client."""
        expiry_time = time.time() + self.auth_ttl
        auth_data = {
            "username": self.username,
            "password": self.password,
            "expiry": str(expiry_time)
        }
        await self.redis_client.setex(self.redis_key, self.auth_ttl, json.dumps(auth_data))

    async def _generate_message_id(self) -> str:
        """Generates a unique message ID using UUID."""
        return 'abc0000001'

    async def _build_message(self, recipient: str, text: str, message_id: Optional[str] = None) -> dict:
        """Encapsulated method to build a message specific to PlayMobile."""
        if message_id is None:
            message_id = await self._generate_message_id()
        return {
            "recipient": recipient,
            "message-id": message_id,
            "sms": {
                "originator": self.originator,
                "content": {
                    "text": text
                }
            }
        }

    async def _build_messages(self, recipients: list[dict]):
        """Generator that builds messages for a list of recipients."""
        for rec in recipients:
            yield await self._build_message(
                recipient=rec["phone"],
                text=rec["text"],
                message_id=rec.get("message_id")  # Allows overriding auto-generated ID if provided
            )

    async def execute_request(self, json_data: dict) -> bool:
        """Executes the HTTP request to send the message, handling token expiration."""
        auth = await self.get_auth()
        print(json_data)
        async with aiohttp.ClientSession() as session:
            async with session.post(self.base_url, auth=auth, json=json_data) as response:
                if response.status == 401:
                    async with session.post(self.base_url, auth=auth, json=json_data) as retry_response:
                        print(retry_response.status, retry_response._body)
                        return retry_response.status == 200
                print(response.status, response._body, response.reason)
                return response.status == 200

    async def send_message(self, recipients: list[dict]) -> bool:
        """Orchestrates the message sending process."""
        messages = [message async for message in self._build_messages(recipients)]
        return await self.execute_request({"messages": messages})


async def get_playmobile(redis_client: ICasheClient = Depends(get_redis_client)):
    return BrokerClient(
        base_url=settings.sms_broker.url,
        username=settings.sms_broker.username,
        password=settings.sms_broker.password,
        originator=settings.sms_broker.originator,
        redis_client=redis_client
    )
