"""Channel monitoring."""

import random
import time
from typing import Optional

from loguru import logger

from .client import KickClient


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
