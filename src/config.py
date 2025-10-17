"""Configuration management."""

import json
from dataclasses import dataclass


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
