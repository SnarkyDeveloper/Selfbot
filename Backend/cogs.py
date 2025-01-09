import json
from Backend.bot import bot
from Backend.utils import read_settings
with open('modules.json') as f:
    modules = json.load(f)

loaded = []

async def setup_cogs():
    if read_settings().get('main').get('first_run') == 'True':
        await bot.load_extension('Backend.Modules.setup')
        return
    for module, enabled in modules['loaded'].items():
        if enabled:
            if module == 'economy':
                print("Cogs loaded, loading economy module...")
                economy_modules = [
                    'work', 'daily', 'steal', 'balance', 'store', 'stripper',
                    'mafia', 'coinflip', 'roulette', 'slots', 'dice'
                ]
                for econ_module in economy_modules:
                    await bot.load_extension(f'Backend.Modules.Economy.{econ_module}')
                    loaded.append(f'Eco{econ_module.capitalize()}')
            else:
                await bot.load_extension(f'Backend.Modules.{module}')
                loaded.append(module.capitalize())
    
    print("--------------------------------")
    print(f"Cogs loaded: {', '.join(loaded)}")
    print("--------------------------------")