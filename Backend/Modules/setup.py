import discord
from discord.ext import commands
from Backend.bot import bot
import json
import os
from Backend.utils import is_owner
path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def setup(self, ctx):
        if ctx.author.id != ctx.guild.owner.id:
            return await ctx.send("Only the server owner can run this command.")
        if not is_owner(ctx.author.id):
            return await ctx.send("You are not allowed to run this command.")
        channel = ctx.channel
        if not channel.permissions_for(ctx.guild.me).manage_webhooks:
            await ctx.send("I don't have permission to manage webhooks in this channel.")
            return
        try:
            webhook = await channel.create_webhook(name=f"{ctx.author.global_name}")
            await ctx.send(f"Webhook created successfully!")
            try:
                webhook_file_path = f'{path}/data/webhook.json'
                if os.path.exists(webhook_file_path):
                    with open(webhook_file_path, 'r') as f:
                        data = json.load(f)
                else:
                    data = {}
                data.update({'webhook_url': webhook.url})
                with open(webhook_file_path, 'w') as f:
                    json.dump(data, f, indent=4)
            except Exception as e:
                await ctx.send(f'Error writing to webhook file: {e}')
                return
            await ctx.send('Please start the bot again to apply the changes.')
            await bot.close()
        except discord.Forbidden:
            await ctx.send("I couldn't create a webhook due to permission issues.")
            return
        except discord.HTTPException as e:
            await ctx.send(f"An error occurred while creating the webhook: {e}")
            return
async def setup(bot):
    await bot.add_cog(Setup(bot))
