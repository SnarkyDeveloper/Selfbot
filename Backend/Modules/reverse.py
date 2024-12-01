import discord
from discord.ext import commands
from Backend.utils import check_permissions
import httpx
class Reverse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    def reverse_search(self, image_url):
        url = "https://google-reverse-image-api.vercel.app/reverse"
        data = {
            "imageUrl": image_url
        }
        response = httpx.post(url, json=data)
        if response.is_success:
            return response.json()
        else:
            return response.status_code
        
    @commands.command(name="reverse", description="Reverse search an image")
    async def reverse(self, ctx, position: int = 0, image_url: str = None):
        if not check_permissions(ctx.author):
            return
        if image_url is None:
            if ctx.message.attachments:
                image_url = ctx.message.attachments[0].url
            elif ctx.message.reference:
                referenced_msg = await ctx.fetch_message(ctx.message.reference.message_id)
                if referenced_msg.attachments:
                    image_url = referenced_msg.attachments[0].url
                elif referenced_msg.embeds and referenced_msg.embeds[0].image:
                    image_url = referenced_msg.embeds[0].image.url
                else:
                    await ctx.send("The referenced message doesn't contain an image")
                    return
            else:
                await ctx.send("Please provide an image URL or attach an image to the message")
                return

        try:
            result = self.reverse_search(image_url)
            
            if isinstance(result, int):
                await ctx.send(f"Error: Received status code {result}")
                return
                
            if not isinstance(result, list):
                await ctx.send("Invalid response from reverse image search")
                return
                
            if not result:
                await ctx.send("No results found")
                return
                
            if position >= len(result):
                await ctx.send(f"Position {position} is out of range. Only {len(result)} results available.")
                return
                
            await ctx.send(result[position])
        except httpx.RequestError as e:
            await ctx.send(f"Error making request: {str(e)}")
        except Exception as e:
            await ctx.send(f"Error processing result: {str(e)}")

async def setup(bot):
    await bot.add_cog(Reverse(bot))