import discord
from Backend.embed import CreateEmbed
import aiohttp
import os
channel_cache = None

create_embed = CreateEmbed()
async def send(bot, ctx, title, content=None, color=None, image=None):
    global channel_cache
    try:
        async with ctx.typing():
            try:
                webhook = await create_embed.embed(ctx, title=title, content=content, color=color, image=image)
            except Exception as e:
                webhook = await create_embed.embed(ctx, title='Error', content=f"An error occurred: {e}", color=0xFF0000)
            if channel_cache is None:
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