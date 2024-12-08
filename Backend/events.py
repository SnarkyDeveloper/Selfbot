from Backend.bot import bot
def setup_events():
    @bot.event
    async def on_command_error(ctx, error):
        print(f"Error executing command: {error}")
    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user}")
        print("Bot is ready")
        print("--------------------------------")