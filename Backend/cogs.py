from Backend.bot import bot
active = ['calculator', 'choose', 'perms', 'snipe', 'music', 'avatar', 'quote', ' ', 'reverse', "dictionary"]
economy = True
loaded = []
async def setup_cogs():
    if active[0] != " ":
        await bot.load_extension('Backend.Modules.calculator')
        loaded.append("Calculator")
    if active[1] != " ":
        await bot.load_extension('Backend.Modules.choose')
        loaded.append("Choose")
    if active[2] != " ":
        await bot.load_extension('Backend.Modules.perms')
        loaded.append("Perms")
    if active[3] != " ":
        await bot.load_extension('Backend.Modules.snipe')
        loaded.append("Snipe")
    if active[4] != " ":
        await bot.load_extension('Backend.Modules.music')
        loaded.append("Music")
    if active[5] != " ":
        await bot.load_extension('Backend.Modules.avatar')
        loaded.append("Avatar")
    if active[6] != " ":
        await bot.load_extension('Backend.Modules.quote')
        loaded.append("Quote")
    if active[7] != " ":
        await bot.load_extension('Backend.Modules.ollama')
        loaded.append("Ollama")
    if active[8] != " ":
        await bot.load_extension('Backend.Modules.reverse')
        loaded.append("Reverse")
    if active[9] != " ":    
        await bot.load_extension('Backend.Modules.dictionary')
        loaded.append("Dictionary")
# ----------------------Economy-------------------------------------
    if economy == True:
        print("Cogs loaded, loading economy module...")
        await bot.load_extension('Backend.Modules.Economy.work')
        loaded.append("EcoWork")
        await bot.load_extension('Backend.Modules.Economy.daily')
        loaded.append("EcoDaily")
        await bot.load_extension('Backend.Modules.Economy.steal')
        loaded.append("EcoSteal")
        await bot.load_extension('Backend.Modules.Economy.balance')
        loaded.append("EcoBalance")
        await bot.load_extension('Backend.Modules.Economy.store')
        loaded.append("EcoStore")
        await bot.load_extension('Backend.Modules.Economy.stripper')
        loaded.append("EcoStripper")
        await bot.load_extension('Backend.Modules.Economy.mafia')
        loaded.append("EcoMafia")
        await bot.load_extension('Backend.Modules.Economy.coinflip')
        loaded.append("EcoCoinflip")
        await bot.load_extension('Backend.Modules.Economy.roulette')
        loaded.append("EcoRoulette")
        await bot.load_extension('Backend.Modules.Economy.slots')
        loaded.append("EcoSlots")
        await bot.load_extension('Backend.Modules.Economy.dice')
        loaded.append("EcoDice")
    print("--------------------------------")
    print(f"Cogs loaded: {', '.join(loaded)}")
    print("--------------------------------")