import discordwebhook
import json
from datetime import datetime
import os
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

    async def embed(self, ctx, title, content, color=None, image=None):
        if not self.webhook_url:
            raise ValueError("Webhook URL is not provided")

        webhook = discordwebhook.Webhook(url=self.webhook_url)

        embed = discordwebhook.Embed(title=title, description=content, color=color)

        if image:
            embed.set_image(url=image)
        embed.set_footer(text=f'Bot created by SnarkyDev, Command ran at {datetime.now().strftime("%m/%d, %H:%M %p")}')
        embed.set_author(name=ctx.author.global_name, icon_url=ctx.author.display_avatar.url)
        webhook = await webhook.send_async(
            embed=embed,
        )
        return webhook
    async def fetch_embed(self, message):
        webhook = discordwebhook.Webhook(url=webhook_url)
        webhook = await webhook.fetch_async(message)
        return webhook
    async def delete_embed(self, message):
        webhook = discordwebhook.Webhook(url=webhook_url)
        webhook = await webhook.delete_async(message)
        return webhook
