import discord
from discord.ext import commands
from Backend.send import send
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

class Timezones(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Get the time in a specific timezone", aliases=['time', 'tz'])
    async def timezone(self, ctx, timezone_input: str = None):
        if timezone_input is None:
            local_time = datetime.now()
            local_timezone = datetime.now().astimezone().tzinfo
            time = local_time.strftime('%m/%d/%Y | %I:%M:%S %p')
            tz_name = local_timezone.tzname(local_time)
            timezone_input = tz_name
        else:
            if timezone_input.lower() == 'utc':
                local_time = datetime.now(timezone.utc)
                time = local_time.strftime('%m/%d/%Y | %H:%M:%S')
                timezone_input = 'UTC'
            elif timezone_input.startswith("UTC"):
                sign = 1 if timezone_input[3] == '+' else -1
                hours = int(timezone_input[4:])
                utc_offset = timedelta(hours=sign * hours)
                custom_tz = timezone(utc_offset)
                local_time = datetime.now(custom_tz)
                time = local_time.strftime('%m/%d/%Y | %H:%M:%S')
                timezone_input = f"UTC{timezone_input[3:]}"
            else:
                try:
                    local_time = datetime.now(ZoneInfo(timezone_input))
                    time = local_time.strftime('%m/%d/%Y | %I:%M:%S %p')
                except Exception:
                    await send(self.bot, ctx, title='Error', content=f'Invalid timezone: {timezone_input}', color=0xff0000)
                    return

        await send(self.bot, ctx, title=f'Current Time', content=f'{time} in {timezone_input}')

async def setup(bot):
    await bot.add_cog(Timezones(bot))