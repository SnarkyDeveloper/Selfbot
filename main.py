import base64, time, dotenv, os, asyncio, json
from Backend.bot import bot
from Backend.groups import *
from Backend.cogs import setup_cogs
from Backend.events import setup_events
from Backend.logger import logger
dotenv.load_dotenv()
token = base64.b64decode(os.getenv("token")).decode("utf-8")
setup_events()
start_time = time.time()
async def setup_groups():
    bot.eco = eco
async def main():
    try:
        await setup_groups()
        print("Starting setup_cogs...")
        await setup_cogs()
        print("Starting bot...")
        await bot.start(token)
    except Exception as e:
        print(f"Error in main: {str(e)}")
        print(f"Error type: {type(e)}")
        if hasattr(e, 'args'):
            print(f"Error args: {e.args}")
    finally:
        await bot.close()
def handle_exception(loop, context):
    exc = context.get('exception')
    if isinstance(exc, (asyncio.CancelledError, KeyboardInterrupt)) or 'KeyboardInterrupt' in str(context):
        loop.stop()
        return
    loop.default_exception_handler(context)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.set_exception_handler(handle_exception)
    try:
        loop.run_until_complete(main())
    except json.JSONDecodeError as e:
        print(f"Error parsing settings.json: {str(e)}")
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
