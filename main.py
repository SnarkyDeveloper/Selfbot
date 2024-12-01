import discord
from discord.ext import commands
from discord.utils import get
import base64
import dotenv
import os
import json
import asyncio
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
    print(f"Error executing command: {error}")

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
        "server": before.guild.id if before.guild else 'DM',
        "message_link": f"https://discord.com/channels/{before.guild.id if before.guild else '@me'}/{before.channel.id}/{before.id}"
    })
    write_messages(messages_data)

@bot.group(invoke_without_command=True)
async def eco(ctx, *args):
    """Economy commands"""
    print(f"Eco group called with args: {args}")
    
    if not args:
        await ctx.send("Available commands: work, daily, balance, steal, shop, coinflip, mafia, stripper")
        return

    # Split the first argument into command and potential parameters
    command_parts = args[0].split(maxsplit=1)
    command_name = command_parts[0].lower()
    print(f"Parsed command name: {command_name}")

    if command_name == "bal":
        command_name = "balance"
    elif command_name == "stripper":
        command_name = "stripper_cmd"

    
    command = eco.get_command(command_name)
    if command:
        print(f"Executing command: {command.name}")
        
        # Handle user mentions
        for arg in args:
            if '<@' in arg:
                user_id = int(''.join(filter(str.isdigit, arg)))
                member = ctx.guild.get_member(user_id)
                print(f"Found mention, processing member: {member}")
                await ctx.invoke(command, member)
                return
        
        # If there are additional parameters, pass them to the command
        if len(command_parts) > 1 or len(args) > 1:
            # Get all parameters after the command name
            params = command_parts[1] if len(command_parts) > 1 else args[1]
            # Convert to int if the command is coinflip
            if command_name == "coinflip":
                params = int(params)
            await ctx.invoke(command, params)
        else:
            await ctx.invoke(command)
    else:
        print(f"Command not found: {command_name}")
        await ctx.send(f"Unknown command: {command_name}")

bot.eco = eco

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("Bot is ready")
    print("--------------------------------")
loaded = []
async def setup_cogs():
    await bot.load_extension('Backend.Modules.calculator')
    loaded.append("Calculator")
    await bot.load_extension('Backend.Modules.choose')
    loaded.append("Choose")
    await bot.load_extension('Backend.Modules.perms')
    loaded.append("Perms")
    await bot.load_extension('Backend.Modules.snipe')
    loaded.append("Snipe")
    await bot.load_extension('Backend.Modules.music')
    loaded.append("Music")
    await bot.load_extension('Backend.Modules.avatar')
    loaded.append("Avatar")
    await bot.load_extension('Backend.Modules.quote')
    loaded.append("Quote")
    await bot.load_extension('Backend.Modules.ollama')
    loaded.append("Ollama")
    await bot.load_extension('Backend.Modules.reverse')
    loaded.append("Reverse")
    
# ----------------------Economy-------------------------------------
    print("Cogs loaded, loading economy module...")
    await bot.load_extension('Backend.Modules.Economy.work')
    loaded.append("EcoWork")
    await bot.load_extension('Backend.Modules.Economy.daily')
    loaded.append("EcoDaily")
    await bot.load_extension('Backend.Modules.Economy.steal')
    loaded.append("EcoSteal")
    await bot.load_extension('Backend.Modules.Economy.balance')
    loaded.append("EcoBalance")
    await bot.load_extension('Backend.Modules.Economy.store')
    loaded.append("EcoStore")
    await bot.load_extension('Backend.Modules.Economy.stripper')
    loaded.append("EcoStripper")
    await bot.load_extension('Backend.Modules.Economy.mafia')
    loaded.append("EcoMafia")
    await bot.load_extension('Backend.Modules.Economy.coinflip')
    loaded.append("EcoCoinflip")
    await bot.load_extension('Backend.Modules.Economy.roulette')
    loaded.append("EcoRoulette")
    await bot.load_extension('Backend.Modules.Economy.slots')
    loaded.append("EcoSlots")
    await bot.load_extension('Backend.Modules.Economy.dice')
    loaded.append("EcoDice")
    print("--------------------------------")
    print(f"Cogs loaded: {', '.join(loaded)}")
    print("--------------------------------")
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
    finally:
        await bot.close()

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

def handle_exception(loop, context):
    exc = context.get('exception')
    if isinstance(exc, (asyncio.CancelledError, KeyboardInterrupt)) or 'KeyboardInterrupt' in str(context):
        loop.stop()
        return
    loop.default_exception_handler(context)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.set_exception_handler(handle_exception)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()