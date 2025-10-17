# Kick Points Miner

Automated bot for mining channel points on Kick.com through periodic chat interactions across multiple channels.

## Features

- Multi-channel concurrent monitoring
- Livestream detection with automatic message sending
- Configurable timing intervals with randomization
- Structured logging with Loguru
- Clean, typed Python architecture

## Installation

```bash
git clone https://github.com/yourusername/kick-points-miner.git
cd kick-points-miner
pip install -r requirements.txt
```

## Configuration

Copy `config.example.json` to `config.json` and configure:

```json
{
  "channels": ["channel1", "channel2"],
  "authorization": "Bearer YOUR_TOKEN_HERE",
  "wait_times": {
    "livestream_active": { "min": 120, "max": 300 },
    "livestream_inactive": 300,
    "error_wait": 180
  },
  "messages": ["[emote:1730752:emojiAngel]", "[emote:1730753:emojiAngry]"]
}
```

**Obtaining Authorization Token:**

1. Open any Kick.com livestream
2. Open Developer Tools (F12) → Network tab
3. Send a chat message
4. Locate request to `https://kick.com/api/v2/messages/send/XXXXX`
5. Copy the `Authorization` header value (starts with "Bearer")

## Usage

### Standard Python

```bash
python main.py
```

### Docker

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## Project Structure

```
src/
├── config.py    # Configuration management
├── client.py    # Kick.com API client
├── monitor.py   # Channel monitoring logic
└── miner.py     # Orchestration layer
```

## Requirements

- Python 3.10+
- Dependencies: `cloudscraper`, `loguru`

## License

[MIT](LICENSE)

## Disclaimer

Educational purposes only. Use in accordance with Kick.com Terms of Service.
