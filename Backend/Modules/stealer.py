import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, PartialEmojiConverter
import aiohttp
import os
import io
from Backend.send import send
class Stealer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def download_asset(self, url, file_path):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    with open(file_path, 'wb') as file:
                        file.write(await response.read())
                    return True
                return False

    @commands.command(description="Steal emojis and stickers")
    @has_permissions(manage_emojis=True)
    async def steal(self, ctx, *emojis: discord.PartialEmoji):
        try:
            stolen_assets = []
            
            if ctx.message.reference:
                message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                
                for sticker in message.stickers:
                    file_extension = 'json' if sticker.format == discord.StickerFormatType.lottie else 'png'
                    file_path = f"{sticker.id}.{file_extension}"
                    
                    if await self.download_asset(sticker.url, file_path):
                        with open(file_path, 'rb') as image_file:
                            try:
                                added = await ctx.guild.create_sticker(
                                    name=sticker.name,
                                    description=f"Stolen by {ctx.author}",
                                    emoji="👍",
                                    file=discord.File(image_file),
                                    reason=f'Stolen by {ctx.author}'
                                )
                                stolen_assets.append(f"Sticker: {added.name}")
                            except Exception as e:
                                print(f"Error creating sticker {sticker.name}: {e}")
                        os.remove(file_path)
                
                for word in message.content.split():
                    if word.startswith("<:") or word.startswith("<a:"):
                        emoji = discord.PartialEmoji.from_str(word)
                        emojis = (*emojis, emoji)

            for emoji in emojis:
                if not isinstance(emoji, discord.PartialEmoji):
                    emoji = discord.PartialEmoji.from_str(str(emoji))
                
                file_extension = 'gif' if emoji.animated else 'png'
                file_path = f"{emoji.id}.{file_extension}"
                emoji_url = f"https://cdn.discordapp.com/emojis/{emoji.id}.{file_extension}"
                
                if await self.download_asset(emoji_url, file_path):
                    with open(file_path, 'rb') as image_file:
                        try:
                            added = await ctx.guild.create_custom_emoji(
                                name=emoji.name,
                                image=image_file.read(),
                                reason=f'Stolen by {ctx.author} with name {emoji.name}'
                            )
                            stolen_assets.append(f"Emoji: :{added.name}:")
                        except:
                            pass
                    os.remove(file_path)

            if stolen_assets:
                content = "Successfully stolen:\n" + "\n".join(stolen_assets)
                await send(self.bot, ctx, title='Assets Stolen', content=content, color=0x2ECC71)
            else:
                await send(self.bot, ctx, title='Error', content="No assets were found to steal.", color=0xff0000)
        except discord.Forbidden:
            await send(self.bot, ctx, title='Error', content="Missing permissions. I need `Manage Emojis` and `Manage Stickers` permissions.", color=0xff0000)
        except Exception as e:
            print(f"Error: {e}")
            await send(self.bot, ctx, title='Error', content=f"An error occurred while stealing assets.", color=0xff0000)

async def setup(bot):
    await bot.add_cog(Stealer(bot))
