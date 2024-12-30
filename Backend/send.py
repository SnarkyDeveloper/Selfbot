import discord
from Backend.embed import CreateEmbed
import aiohttp
import os
channel_cache = None

create_embed = CreateEmbed()

async def upload_to_0x0_st(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    url = "https://0x0.st"
    async with aiohttp.ClientSession() as session:
        with open(file_path, "rb") as file:
            async with session.post(url, data={"file": file}) as response:
                if response.status == 200:
                    result = await response.text()
                    return result.strip()
                else:
                    raise Exception(f"Failed to upload file to 0x0.st. Status code: {response.status}")
async def send(bot, ctx, title, content=None, color=None, image=None):
    global channel_cache
    try:
        if image and not image.startswith("http"):
            image = await upload_to_0x0_st(image)
        webhook = await create_embed.embed(ctx, title=title, content=content, color=color, image=image)
        if channel_cache is None or channel_cache.id != int(webhook.channel_id):
            channel_cache = bot.get_channel(int(webhook.channel_id))
        message = await channel_cache.fetch_message(int(webhook.id))
        message = await message.forward(ctx.channel)
        return message
    except discord.Forbidden:
        await ctx.send("I don't have permission to embed links in this channel.")
    except discord.HTTPException:
        print("An error occurred while sending the message.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")