import random
from discord.ext import commands
from Backend.utils import read_messages, write_messages
from Backend.send import send
class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Snipe a deleted message. Optional: specify position (e.g. >s 2)', aliases=['s'])
    async def snipe(self, ctx, position=1):
        try:
            position = int(position)
        except ValueError:
            await send(self.bot, ctx, title='Error', content="Please provide a valid number for position", color=0xff0000)
            return
            
        messages_data = read_messages()
        if len(messages_data["messages"]) > 0:
            current_location = ctx.guild.id if ctx.guild else 'DM'
            
            location_messages = [
                msg for msg in messages_data["messages"] 
                if (msg.get("server") == current_location) and msg["type"] == "delete"
            ]
            
            if location_messages:
                if 1 <= position <= len(location_messages):
                    msg = location_messages[-position]
                    response = f"{msg['message']}"
                    await send(self.bot, ctx, title=f'Message Deleted by {msg["user"]}', content=response, color=0xFEE75C)
                else:
                    await send(self.bot, ctx, title='Error', content=f"Invalid position. Available range: 1-{len(location_messages)}", color=0xff0000)
            else:
                await send(self.bot, ctx, title='Error', content="No deleted messages to snipe here", color=0xff0000)
        else:
            await send(self.bot, ctx, title='Error', content="No messages to snipe", color=0xff0000)

    @commands.command(description='Snipe an edited message. Optional: specify position (e.g. >es 2)', aliases=['es'])
    async def editsnipe(self, ctx, position=1):
        try:
            position = int(position)
        except ValueError:
            await send(self.bot, ctx, title='Error', content="Please provide a valid number for position", color=0xff0000)
            return
        messages_data = read_messages()
        if len(messages_data["messages"]) > 0:
            current_location = ctx.guild.id if ctx.guild else 'DM'
            
            location_messages = [
                msg for msg in messages_data["messages"] 
                if (msg.get("server") == current_location) and msg["type"] == "edit"
            ]
            
            if location_messages:
                if 1 <= position <= len(location_messages):
                    msg = location_messages[-position]
                    response = f"\n**Before:** {msg['message_before']}\n**After:** {msg['message_after']}\n[Jump to message]({msg['message_link']})"
                    await send(self.bot, ctx, title=f'Message Edited by {msg["user"]}', content=response, color=0xFEE75C)
                else:
                    await send(self.bot, ctx, title='Error', content=f"Invalid position. Available range: 1-{len(location_messages)}", color=0xff0000)
            else:
                await send(self.bot, ctx, title='Error', content="No edited messages to snipe here", color=0xff0000)
        else:
            await send(self.bot, ctx, title='Error', content="No messages to snipe", color=0xff0000)

    @commands.is_owner()
    @commands.command(description='Clear the snipe cache', aliases=['cs'])
    async def clearsnipe(self, ctx):
        messages_data = read_messages()
        messages_data["messages"] = []
        write_messages(messages_data)
        await send(self.bot, ctx, title='Success', content="Snipe cache cleared", color=0x2ECC71)

async def setup(bot):
    await bot.add_cog(Snipe(bot))