import json
import random
import threading
import time
from dataclasses import dataclass
from typing import Optional

import cloudscraper
from loguru import logger


@dataclass
class Config:
    """Application configuration."""

    channels: list[str]
    messages: list[str]
    authorization: str
    wait_times: dict[str, int | dict[str, int]]

    @classmethod
    def load(cls, path: str = "config.json") -> "Config":
        """Load configuration from JSON file."""
        with open(path, "r") as f:
            data = json.load(f)
        return cls(**data)


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


class ChannelMonitor:
    """Monitors a single Kick.com channel and sends messages."""

    def __init__(
        self,
        username: str,
        client: KickClient,
        messages: list[str],
        wait_times: dict[str, int | dict[str, int]],
    ):
        self.username = username
        self.client = client
        self.messages = messages
        self.wait_times = wait_times

    def check_and_send(self) -> tuple[bool, Optional[str]]:
        """Check if channel is live and send a message if so."""
        channel_data = self.client.get_channel(self.username)

        if not channel_data:
            return False, None

        if channel_data.get("livestream") is None:
            return False, None

        chatroom_id = channel_data.get("chatroom", {}).get("id")
        if not chatroom_id:
            return False, None

        message = random.choice(self.messages)
        success = self.client.send_message(chatroom_id, message)

        return success, message if success else None

    def run(self) -> None:
        """Run the monitoring loop."""
        while True:
            try:
                sent, message = self.check_and_send()

                if sent:
                    wait_time = random.randint(
                        self.wait_times["livestream_active"]["min"],
                        self.wait_times["livestream_active"]["max"],
                    )
                    logger.info(
                        f"Sent to {self.username}: {message}. Waiting {wait_time}s."
                    )
                else:
                    wait_time = self.wait_times["livestream_inactive"]
                    logger.info(f"{self.username} is offline. Waiting {wait_time}s.")

                time.sleep(wait_time)
            except Exception as e:
                logger.error(f"Error monitoring {self.username}: {e}")
                time.sleep(self.wait_times.get("error_wait", 60))


class PointsMiner:
    """Orchestrates mining points across multiple channels."""

    def __init__(self, config: Config):
        self.config = config
        self.client = KickClient(config.authorization)
        self.monitors: list[ChannelMonitor] = []

    def start(self) -> None:
        """Start monitoring all configured channels."""
        threads = []

        for username in self.config.channels:
            monitor = ChannelMonitor(
                username=username,
                client=self.client,
                messages=self.config.messages,
                wait_times=self.config.wait_times,
            )
            self.monitors.append(monitor)

            thread = threading.Thread(target=monitor.run, daemon=True)
            threads.append(thread)
            thread.start()

        logger.success(f"Started monitoring {len(self.config.channels)} channels")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down...")


def main() -> None:
    """Application entry point."""
    config = Config.load()
    miner = PointsMiner(config)
    miner.start()


if __name__ == "__main__":
    main()
