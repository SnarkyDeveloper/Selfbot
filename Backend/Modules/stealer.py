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

    @commands.command(description="Steal an emoji")
    @has_permissions(manage_emojis=True)
    async def steal(self, ctx, emoji: discord.PartialEmoji = None):
        try:
            if emoji is None:
                print("No emoji provided, looking for one in the message")
                message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                for e in message.content.split():
                    if e.startswith("<:") or e.startswith("<a:"):
                        emoji = discord.PartialEmoji.from_str(e)
                        print(f"Found emoji {emoji}")
                        break
                else:
                    await ctx.send("No emoji found in the message.")
                    return

            print(f"Emoji is {emoji} with type {type(emoji)}")
            if type(emoji) != discord.PartialEmoji:
                emoji = discord.PartialEmoji.from_str(emoji)
            
            emoji_url = f"https://cdn.discordapp.com/emojis/{emoji.id}.{'gif' if emoji.animated else 'png'}"
            print(f"Emoji URL: {emoji_url}")
            async with aiohttp.ClientSession() as session:
                async with session.get(emoji_url) as response:
                    if response.status == 200:
                        file_extension = 'gif' if emoji.animated else 'png'
                        file_path = f"{emoji.id}.{file_extension}"
                        with open(file_path, 'wb') as file:
                            file.write(await response.read())
                        print(f"Saved emoji as {file_path}")

                        with open(file_path, 'rb') as image_file:
                            added = await ctx.guild.create_custom_emoji(
                                name=emoji.name,
                                image=image_file.read(),
                                reason=f'Stolen by {ctx.author} with name {emoji.name}'
                            )
                            print(f"Created custom emoji {added.name}")

                        message = await send(self.bot, ctx, title='Emoji stolen', content=f"Emoji {added.name} stolen! Use it with `:{added.name}:`", color=0x2ECC71)
                        if not emoji.animated:
                            await message.add_reaction(added)

                        os.remove(file_path)
                        print(f"Deleted the saved file {file_path}")

                    else:
                        print(f"Failed to fetch emoji image: {response.status}")
                        await send(self.bot, ctx, title='Error', content=f"Failed to fetch emoji image from the server, status code: {response.status}", color=0xff0000)
        except discord.Forbidden:
            print("No permissions to add emojis")
            await send(self.bot, ctx, title='Error', content="No permissions to add emojis, please give me the `Manage Emojis` permission.", color=0xff0000)
        except Exception as e:
            print(f"Error: {e}")
            await send(self.bot, ctx, title='Error', content=f"An error occurred while trying to steal the emoji.", color=0xff0000)

async def setup(bot):
    await bot.add_cog(Stealer(bot))
