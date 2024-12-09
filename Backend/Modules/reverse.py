import discord
from discord.ext import commands
import sys
import httpx
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import quote, urlsplit, urlunsplit
results = []
sys.stdout.reconfigure(encoding='utf-8')
def reverse_search(image_url):
    search_url = f"https://yandex.com/images/search?rpt=imageview&url={quote(image_url)}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.60 Safari/537.36'
    }
    response = httpx.get(search_url, headers=headers)
    print(search_url)
    if response.status_code != 200:
        print("Failed to retrieve results")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    root_div = soup.find('div', id=lambda x: x and x.startswith('CbirSites_simple'))
    if not root_div:
        print("No sites section found")
        return None

    data_state = root_div.get('data-state')
    if not data_state:
        print("No data-state found in the section")
        return None

    try:
        data = json.loads(data_state)
        sites = data.get('sites', [])
        return [{'title': site['title'], 'url': site['url']} for site in sites]
    except json.JSONDecodeError:
        print("Failed to parse JSON")
        return None

def is_english_text(text):
    return bool(re.match(r'^[\x00-\x7F]*$', text))

class Reverse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Reverse image search using Yandex", aliases=["rev", "yandex"])
    async def reverse(self, ctx, image_url: str = None):
        if not image_url:
            if ctx.message.reference:
                message = await ctx.fetch_message(ctx.message.reference.message_id)
                if message.attachments:
                    image_url = message.attachments[0].url
                else:
                    await ctx.send("Please provide an image or reply to an image.")
                    return
            else:
                await ctx.send("Please provide an image or reply to an image.")
                return
        
        sites = reverse_search(image_url)
        if sites:
            message = ""
            for idx, site in enumerate(sites, start=1):
                if is_english_text(site['title']) and is_english_text(site['url']):
                    message += f"{site['title']}: {site['url']}\n"
            await ctx.send(f'# Results:\n{message}')
        else:
            await ctx.send("No matching sites found.")


async def setup(bot):    
    await bot.add_cog(Reverse(bot))
