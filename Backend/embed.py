import discordwebhook
import json
from datetime import datetime
import os
import httpx
import asyncio
import aiofiles
import discord

path = os.path.dirname(os.path.dirname(__file__))
if not os.path.exists(f'{path}/data/webhook.json'):
    with open(f'{path}/data/webhook.json', 'w') as f:
        json.dump({'webhook_url': None}, f)
with open(f'{path}/data/webhook.json') as f:
    try:
        data = json.load(f)
        webhook_url = data['webhook_url']
    except:
        webhook_url = None

class CreateEmbed:
    def __init__(self):
        self.webhook_url = webhook_url
    async def send_file(self, file, webhook):
        if not os.path.exists(file):
            print("File does not exist")
            return None

        async with aiofiles.open(file, 'rb') as f:
            file_content = await f.read()

        files = {
            'file': (os.path.basename(file), file_content)
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(webhook, files=files)

        if response.status_code == 200:
            response_data = response.json()
            return response_data['attachments'][0]['url']
        else:
            print(f'Failed to send file: {response.status_code}, {response.text}')
            return None

    async def embed(self, ctx, title, content, color=0x000000, image=None, video=None):
        if not self.webhook_url:
            raise ValueError("Webhook URL is not provided")
        if image and not image.startswith("http") or video and not video.startswith("http"):
                image = await self.send_file(file=f'{image}', webhook=self.webhook_url)
        webhook = discordwebhook.Webhook(url=self.webhook_url)
        try:
            embed = discordwebhook.Embed(title=title, description=content, color=color)
            if image:
                embed.set_image(url=image)
            if video:
                embed.set_video(url=video)
            embed.set_footer(text=f'Bot created by SnarkyDev, Command ran at {datetime.now().strftime("%m/%d, %I:%M %p")}')
            embed.set_author(name=ctx.author.global_name, icon_url=ctx.author.display_avatar.url)
            webhook = await webhook.send_async(
                embed=embed,
            )
            return webhook
        except Exception as e:
            raise e
    async def fetch_embed(self, message):
        webhook = discordwebhook.Webhook(url=webhook_url)
        webhook = await webhook.fetch_async(message)
        return webhook
    async def delete_embed(self, message):
        webhook = discordwebhook.Webhook(url=webhook_url)
        webhook = await webhook.delete_async(message)
        return webhook
