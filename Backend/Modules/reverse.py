import discord
from discord.ext import commands
from Backend.utils import check_permissions
import httpx
from bs4 import BeautifulSoup
def reverse_image_search_yandex(image_url):
    search_url = f"https://yandex.com/images/search?rpt=imageview&url={image_url}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = httpx.get(search_url, headers=headers)
    
    if response.status_code != 200:
        print("Failed to retrieve results")
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    result = None
    for img_tag in soup.find_all('img'):
        img_url = img_tag.get('src')
        if img_url and img_url.startswith('http'):
            result = img_url
            break
    
    return result
class Reverse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(description="Reverse image search using Yandex")
    async def reverse_image_search_yandex(self, ctx, image_url: str = None):
        if not image_url:
            if not ctx.attachments[0]:
                if ctx.message.reference:
                    message = await ctx.fetch_message(ctx.message.reference.message_id)
                    if message.attachments:
                        image_url = message.attachments[0].url
                    else:
                        await ctx.send("Please provide an image or reply to an image")
                        return
                else:
                    await ctx.send("Please provide an image or reply to an image")
                    return
            else:
                image_url = ctx.attachments[0].url
        top_match_yandex = reverse_image_search_yandex(image_url)
        await ctx.send(content="Top Match Image:", file=discord.File(top_match_yandex))
async def setup(bot):    
    await bot.add_cog(Reverse(bot))