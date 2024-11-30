import discord
from discord.ext import commands
from discord.utils import get
import base64
import dotenv
import os
import json
from Backend.utils import check_permissions

dotenv.load_dotenv()
description = "Selfbot"
token = base64.b64decode(os.getenv("token")).decode("utf-8")
def read_messages():
    try:
        with open('messages.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"messages": []}

def write_messages(data):
    with open('messages.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

class CustomBot(commands.Bot):
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.content.startswith('>'):
            if check_permissions(message.author):
                try:
                    parts = message.content[1:].split(maxsplit=1)
                    command_name = parts[0]
                    
                    command = self.get_command(command_name)
                    if command:
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
    command_prefix='>', 
    description=description, 
    self_bot=True,
    status=discord.Status.dnd,
    help_command=None
)

class CommandHelper:
    def __init__(self, ctx):
        self.ctx = ctx
    
    async def send(self, message):
        channel = self.ctx.message.channel
        try:
            await channel.send(message)
        except discord.Forbidden:
            await self.ctx.message.edit(content=message)

@bot.event
async def on_command_error(ctx, error):
    print(f"An error occurred: {str(error)}")
    print(f"Error type: {type(error)}")
    if isinstance(error, commands.CommandInvokeError):
        print(f"Original error: {error.original}")
        if "40001" in str(error):
            await ctx.send("Unable to perform this action - Discord permission error")

@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return
    user = message.author
    messages_data = read_messages()
    messages_data["messages"].append({
            "user": str(user),
            "message": message.content,
            "type": "delete",
            "server": message.guild.id if message.guild else 'DM'
    })
    write_messages(messages_data)

@bot.event
async def on_message_edit(before, after):
    if before.author.bot:
        return
    messages_data = read_messages()
    messages_data["messages"].append({
        "user": str(before.author),
        "message_before": before.content,
        "message_after": after.content,
        "type": "edit",
        "server": before.guild.id if before.guild else 'DM'
    })
    write_messages(messages_data)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("Bot is ready")
    print("--------------------------------")
async def setup_cogs():
    await bot.load_extension('Backend.Modules.calculator')
    await bot.load_extension('Backend.Modules.choose')
    await bot.load_extension('Backend.Modules.perms')
    await bot.load_extension('Backend.Modules.snipe')
    await bot.load_extension('Backend.Modules.music')
    print("Cogs loaded")
    
async def main():
    try:
        print("Starting setup_cogs...")
        await setup_cogs()
        print("Starting bot...")
        await bot.start(token)
    except Exception as e:
        print(f"Error in main: {str(e)}")
        print(f"Error type: {type(e)}")
        if hasattr(e, 'args'):
            print(f"Error args: {e.args}")

@bot.command(name='help', description="Shows this message")
async def help_command(ctx, command_name=None):
    if command_name:
        command = bot.get_command(command_name)
        if command:
            await ctx.send(f"Help for {command_name}: {command.help}")
        else:
            await ctx.send(f"Command '{command_name}' not found.")
    else:
        commands_list = [f"`{command.name}`: {command.description}" for command in bot.commands]
        await ctx.send("Available commands:\n" + "\n".join(commands_list))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())