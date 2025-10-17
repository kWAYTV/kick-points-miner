"""Kick.com API client."""

import random
from typing import Optional

import cloudscraper
from loguru import logger


class KickClient:
    """Client for interacting with Kick.com API."""

    BASE_URL = "https://kick.com/api/v2"

    def __init__(self, authorization: str):
        self.authorization = authorization
        self.scraper = cloudscraper.create_scraper()

    def get_channel(self, username: str) -> Optional[dict]:
        """Fetch channel information."""
        try:
            url = f"{self.BASE_URL}/channels/{username}"
            response = self.scraper.get(url)
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching channel {username}: {e}")
            return None

    def send_message(self, chatroom_id: int, content: str) -> bool:
        """Send a message to a chatroom."""
        try:
            url = f"{self.BASE_URL}/messages/send/{chatroom_id}"
            payload = {
                "content": content,
                "type": "message",
                "message_ref": str(random.randint(1000000000000, 9999999999999)),
            }
            headers = {"Authorization": self.authorization}
            self.scraper.post(url, json=payload, headers=headers)
            return True
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False
