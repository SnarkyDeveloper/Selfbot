from Backend.utils import is_owner
from Backend.send import send
from discord.ext import commands
import subprocess
class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Reloads all extensions - BOT OWNER ONLY")
    async def reload(self, ctx):
        if not await is_owner(ctx):
            await send(self.bot, ctx, title='Error', content="You are not allowed to use this command", color=0xff0000)
            return

        results = []
        for ext in list(self.bot.extensions):
            try:
                await self.bot.reload_extension(ext)
                results.append(f"✓ {ext}")
            except Exception as e:
                results.append(f"❌ {ext}")
                print(f"Failed to reload {ext}: {e}")

        status_message = "\n".join(results)
        await send(self.bot, ctx, title='Reload Status', content=f"```\n{status_message}\n```")
    @commands.command(name="push", description="Pushes a new version of the bot - BOT OWNER ONLY")
    async def gh_push(self, ctx, message = "commit"):
        if not await is_owner(ctx):
            await send(self.bot, ctx, title='Error', content="You are not allowed to use this command", color=0xff0000)
            return
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", message])
        subprocess.run(["git", "push"])
        url = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True).stdout.strip()
        await send(self.bot, ctx, title='Push Status', content=f"Pushed successfully, check {url} for changes", color=0x00ff00)
async def setup(bot):
    await bot.add_cog(Reload(bot))
