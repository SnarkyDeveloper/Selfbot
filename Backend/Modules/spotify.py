import discord
from discord.ext import commands
import httpx
import flask
from flask import request
from Backend.utils import read_settings

class Spotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def spotify(self, ctx):
        url = read_settings()["Spotify"].get("redirect_uri")
        httpx.get(url)
        
        
        
def setup(bot):
    bot.add_cog(Spotify(bot))