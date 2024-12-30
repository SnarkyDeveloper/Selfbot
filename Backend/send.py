import discord
from Backend.embed import CreateEmbed
from functools import lru_cache
create_embed = CreateEmbed()
@lru_cache(maxsize=20)
async def send(bot, ctx, title, content = None, color = None, image = None):
    try:
        webhook = await create_embed.embed(ctx, title=title, content=content, color=color, image=image)
        channel = bot.get_channel(int(webhook.channel_id))
        if channel is None:
            await ctx.send("Channel not found.")
            return
        message = await channel.fetch_message(int(webhook.id))
        message = await message.forward(ctx.channel)
        return message
    except discord.Forbidden:
        await ctx.send("I don't have permission to embed links in this channel.")
    except discord.HTTPException:
        print("An error occurred while sending the message.")