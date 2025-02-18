import discord
from discord.ext import commands
import httpx
import json
from Backend.send import send
class github(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(Description="Get information on a github repository", aliases=["gh"])
    async def github(self, ctx, user: str = None, repo: str = None):
        if not user:
            await ctx.send(f'Not in user/repo format! Example: `>github snarkydeveloper/selfbot`')
        if not repo:
            user = user.split('/')
            repo = user[1]
            user = user[0]
        response = httpx.get(f"https://api.github.com/repos/{user}/{repo}")
        if str(response.status_code) != '200':
            await ctx.send(f'Repository not found!')
            return
        response = json.loads(response.text)
        repo_name = response['name']
        repo_description = response['description'] if response['description']=='null' else 'No description'
        repo_url = response['html_url']
        repo_owner= response['owner']['login']
        repo_owner_url = response['owner']['html_url']
        repo_stars = response['stargazers_count']
        repo_top_language = response['language']
        full_repo_name = response['full_name']
        await send(self.bot, ctx, title=f'{repo_name}', content=f'[{full_repo_name}](<{repo_url}>)\nDescription | {repo_description}\nOwner | [{repo_owner}](<{repo_owner_url}>)\nStars | {repo_stars} :star: \nTop Language | {repo_top_language}')
async def setup(bot):
    await bot.add_cog(github(bot))