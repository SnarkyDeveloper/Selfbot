import random
from discord.ext import commands
from Backend.utils import check_permissions, read_messages, write_messages

class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Snipe a deleted message', aliases=['s'])
    async def snipe(self, ctx, *, args=None):
        if args:
            return
        if check_permissions(ctx.author):
            messages_data = read_messages()
            if len(messages_data["messages"]) > 0:
                current_location = ctx.guild.id if ctx.guild else 'DM'
                
                location_messages = [
                    msg for msg in messages_data["messages"] 
                    if (msg.get("server") == current_location) and msg["type"] == "delete"
                ]
                
                if location_messages:
                    latest_msg = location_messages[-1]
                    response = f"**Deleted Message by {latest_msg['user']}**\n{latest_msg['message']}"
                    await ctx.send(response)
                else:
                    await ctx.send("No deleted messages to snipe here")
            else:
                await ctx.send("No messages to snipe")
        else:
            pass

    @commands.command(description='Snipe an edited message', aliases=['es'])
    async def editsnipe(self, ctx, *, args=None):
        if args:
            return
        if check_permissions(ctx.author):
            messages_data = read_messages()
            if len(messages_data["messages"]) > 0:
                current_location = ctx.guild.id if ctx.guild else 'DM'
                
                location_messages = [
                    msg for msg in messages_data["messages"] 
                    if (msg.get("server") == current_location) and msg["type"] == "edit"
                ]
                
                if location_messages:
                    latest_msg = location_messages[-1]
                    response = f"**Message Edit by {latest_msg['user']}**\nBefore: {latest_msg['message_before']}\nAfter: {latest_msg['message_after']}"
                    await ctx.send(response)
                else:
                    await ctx.send("No edited messages to snipe here")
            else:
                await ctx.send("No messages to snipe")
        else:
            pass
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