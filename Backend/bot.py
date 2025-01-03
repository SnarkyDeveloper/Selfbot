import discord
from discord.ext import commands
from Backend.utils import read_settings
from Backend.permissions import check_permissions
description = "Selfbot"
prefix = read_settings()["main"]["prefix"]
class CustomBot(commands.Bot):
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.content.startswith(prefix):
            try:
                parts = message.content[1:].split(maxsplit=1)
                command_name = parts[0]
            
                command = self.get_command(command_name)
                if command:
                    if check_permissions(bot, message) or command_name == 'eco':
                        ctx = await self.get_context(message)
                        try:
                            args = parts[1] if len(parts) > 1 else ''
                            if args:
                                await command(ctx, args)
                            else:
                                await command(ctx)
                        except Exception as e:
                            print(f"Error executing command: {e}")
            except Exception as e:
                print(f"Error in command processing: {e}")
bot = CustomBot(
        command_prefix=read_settings()["main"]["prefix"], 
        description=description, 
        self_bot=True,
        status=discord.Status.dnd,
        activity=discord.Activity(type=discord.ActivityType.playing, name=read_settings()["main"]["status"], buttons=["htttps://github.com/SnarkyDeveloper/Selfbot"]),
        help_command=None,
    )