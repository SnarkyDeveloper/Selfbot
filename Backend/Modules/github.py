import discord
from discord.ext import commands
import httpx
import json
class github(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(Description="Get information on a github repository")
    async def github(self, ctx, user: str, repo: str):
        if not repo or not user:
            await ctx.send(f'Not in user/repo format! Example: `>github snarkydeveloper/selfbot`')
            return
        response = httpx.get(f"https://api.github.com/repos/{user}/{repo}")
        if response.status_code == '404':
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
        await ctx.send(f'# {full_repo_name}\n{repo_name} | {repo_url}\nDescription | {repo_description}\nOwner | [{repo_owner}](<{repo_owner_url}>)\nStars | {repo_stars} :star: \nTop Language | {repo_top_language}')
async def setup(bot):
    await bot.add_cog(github(bot))