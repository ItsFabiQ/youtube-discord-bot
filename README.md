# YouTube Notification Discord Bot

This project is a Discord bot that checks for new videos on a specified YouTube channel and sends a notification to a Discord channel when a new video is uploaded.

## Features

- Monitors a YouTube channel for new video uploads.
- Sends a notification to a specified Discord channel when a new video is detected.
- Runs continuously, checking for new videos at regular intervals.

## Prerequisites

- Python 3.6 or higher
- `discord.py` library
- `google-api-python-client` library

## Installation

1. Clone the repository or download the script.
2. Install the required libraries using pip:
   ```bash
   pip install discord.py google-api-python-client
   ```

## Configuration

1. Create a new Discord bot on the [Discord Developer Portal](https://discord.com/developers/applications) and get the bot token.
2. Obtain a YouTube Data API key from the [Google Developer Console](https://console.developers.google.com/).
3. Set the `discord_token`, `youtube_api_key`, and `channel_id` variables in the script with your bot token, YouTube API key, and the ID of the YouTube channel you want to monitor.

## Usage

1. Run the script:
   ```bash
   python bot.py
   ```
2. The bot will start and begin checking for new videos on the specified YouTube channel. When a new video is found, it will send a notification to the Discord channel.

## Code Explanation

### Main Script

```python
import discord
from googleapiclient.discovery import build
import asyncio

discord_token = ''
youtube_api_key = ''
channel_id = ''

client = discord.Client(intents=discord.Intents.default())

async def check_for_new_videos():
    youtube = build('youtube', 'v3', developerKey=youtube_api_key)

    await client.wait_until_ready()
    old_video_url = 0
    while not client.is_closed():
        try:
            response = youtube.search().list(
                part='snippet',
                channelId=channel_id,
                maxResults=1,
                order='date',
                type='video'
            ).execute()
            if 'items' in response and response['items']:
                video_id = response['items'][0]['id']['videoId']
                video_url = f'https://www.youtube.com/watch?v={video_id}'
                if old_video_url != video_url:
                    channel = client.get_channel()
                    await channel.send(f'@everyone A new video has appeared on my channel - {video_url}')
                    old_video_url = video_url
                    print(old_video_url)
                    print(video_url)
            else:
                print('There are no new videos')
        except Exception as e:
            print('An error occurred while downloading data from YouTube:', e)
        await asyncio.sleep(1800)

@client.event
async def on_ready():
    print(f'Bot is online as {client.user}')
    client.loop.create_task(check_for_new_videos())

client.run(discord_token)
```

### Explanation

- **Imports**: The script imports necessary libraries including `discord`, `googleapiclient.discovery`, and `asyncio`.
- **Configuration Variables**: `discord_token`, `youtube_api_key`, and `channel_id` are placeholders for your bot token, YouTube API key, and YouTube channel ID.
- **Discord Client**: Initializes the Discord client with default intents.
- **check_for_new_videos Function**: This asynchronous function checks for new videos on the specified YouTube channel and sends a notification to the Discord channel if a new video is found.
- **on_ready Event**: This event is triggered when the bot is ready and starts the `check_for_new_videos` task.
- **Running the Bot**: The bot is run using `client.run(discord_token)`.

## License

This project is licensed under the MIT License.
