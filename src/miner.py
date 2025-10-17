"""Points miner orchestration."""

import threading
import time

from loguru import logger

from .client import KickClient
from .config import Config
from .monitor import ChannelMonitor


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
