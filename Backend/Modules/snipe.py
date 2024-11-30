import random
from discord.ext import commands
from Backend.utils import check_permissions, read_messages, write_messages

class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Snipe a deleted message. Optional: specify position (e.g. >s 2)', aliases=['s'])
    async def snipe(self, ctx, position=1):
        # Convert position to int, with error handling
        try:
            position = int(position)
        except ValueError:
            await ctx.send("Please provide a valid number for position")
            return
            
        if not check_permissions(ctx.author):
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
                    response = f"**Deleted Message by {msg['user']}**\n{msg['message']}"
                    await ctx.send(response)
                else:
                    await ctx.send(f"Invalid position. Available range: 1-{len(location_messages)}")
            else:
                await ctx.send("No deleted messages to snipe here")
        else:
            await ctx.send("No messages to snipe")

    @commands.command(description='Snipe an edited message. Optional: specify position (e.g. >es 2)', aliases=['es'])
    async def editsnipe(self, ctx, position=1):
        # Convert position to int, with error handling
        try:
            position = int(position)
        except ValueError:
            await ctx.send("Please provide a valid number for position")
            return
            
        if not check_permissions(ctx.author):
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
                    response = f"**Message Edit by {msg['user']}**\nBefore: {msg['message_before']}\nAfter: {msg['message_after']}\n[Jump to message]({msg['message_link']})"
                    await ctx.send(response)
                else:
                    await ctx.send(f"Invalid position. Available range: 1-{len(location_messages)}")
            else:
                await ctx.send("No edited messages to snipe here")
        else:
            await ctx.send("No messages to snipe")

    @commands.command(description='Clear the snipe cache', aliases=['cs'])
    async def clearsnipe(self, ctx, *, args=None):
        if args:
            return
        if check_permissions(ctx.author):
            messages_data = read_messages()
            messages_data["messages"] = []
            write_messages(messages_data)
            await ctx.send("Snipe cache cleared")
        else:
            pass

async def setup(bot):
    await bot.add_cog(Snipe(bot))