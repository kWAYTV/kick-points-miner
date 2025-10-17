"""Entry point when running as module: python -m src"""

from .config import Config
from .miner import PointsMiner


def main() -> None:
    """Application entry point."""
    config = Config.load()
    miner = PointsMiner(config)
    miner.start()


if __name__ == "__main__":
    main()
