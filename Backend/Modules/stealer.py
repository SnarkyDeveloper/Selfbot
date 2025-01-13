import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import aiohttp
import os
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
    async def steal(self, ctx, *args):
        try:
            stolen_assets = []
            emojis_to_steal = []
            added_emojis = []
            existing_emoji_names = {emoji.name for emoji in ctx.guild.emojis}
            existing_sticker_names = {sticker.name for sticker in ctx.guild.stickers}
            if ctx.message.reference:
                message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            else:
                message = ctx.message

            for sticker in message.stickers:
                if sticker.name in existing_sticker_names:
                    stolen_assets.append(f"❌ Emoji: `{emoji.name}` already exists")
                    continue
                file_extension = 'gif' if sticker.format == discord.StickerFormatType.gif else 'png'
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
                            stolen_assets.append(f"✅ Sticker: `{added.name}`")
                        except Exception as e:
                            print(f"Error creating sticker {sticker.name}: {e}")
                    os.remove(file_path)

            for word in message.content.split():
                if word.startswith("<:") or word.startswith("<a:"):
                    try:
                        emoji = discord.PartialEmoji.from_str(word)
                        emojis_to_steal.append(emoji)
                    except:
                        continue

            for arg in args:
                if str(arg).startswith("<:") or str(arg).startswith("<a:"):
                    try:
                        emoji = discord.PartialEmoji.from_str(str(arg))
                        emojis_to_steal.append(emoji)
                    except:
                        continue

            for emoji in emojis_to_steal:
                if emoji.name in existing_emoji_names:
                    stolen_assets.append(f"❌ Emoji: `{emoji.name}` already exists")
                    continue
                    
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
                            stolen_assets.append(f"✅ Emoji Added: `:{added.name}:`")
                            added_emojis.append(added)
                        except:
                            pass
                    os.remove(file_path)

            try:
                for emoji in added_emojis:
                    try:
                        await ctx.message.add_reaction(emoji)
                    except:
                        continue
            except:
                pass

            if stolen_assets:
                newline = '\n'
                content = f"Successfully stolen: {newline}{'{newline}'.join(stolen_assets)}"
                await send(self.bot, ctx, title='Assets Stolen', content=f'{content} \nStolen By {ctx.author.mention}', color=0x2ECC71)
            else:
                await send(self.bot, ctx, title='Error', content="No assets were found to steal.", color=0xff0000)
        except discord.Forbidden:
            await send(self.bot, ctx, title='Error', content="Missing permissions. I need `Manage Emojis` and `Manage Stickers` permissions.", color=0xff0000)
        except Exception as e:
            print(f"Error: {e}")
            await send(self.bot, ctx, title='Error', content=f"An error occurred while stealing assets.", color=0xff0000)

async def setup(bot):
    await bot.add_cog(Stealer(bot))
