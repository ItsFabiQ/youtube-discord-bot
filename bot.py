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
                if(old_video_url != video_url):
                    channel = client.get_channel()
                    await channel.send(f'@everyone A new video has appeared on my channel - {video_url}')
                    old_video_url = video_url
            else:
                print('There are no new videos')
        except Exception as e:
            print('An error occurred while downloading data from YouTube:', e)
        await asyncio.sleep(1800) 

@client.event
async def on_ready():
    print(f'Bot is online as {client.user}')
    client.loop.create_task(check_for_new_videos())
