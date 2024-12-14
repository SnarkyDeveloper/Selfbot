from Backend.bot import bot
calculator = True
choose = True
perms = True
snipe = True
music = True
avatar = True
quote = True
ollama = False
reverse = True
dictionary = True
afk = True
qotd = True
lyrics = True
#--------
economy = True
help = True
loaded = []
async def setup_cogs():
    if calculator:
        await bot.load_extension('Backend.Modules.calculator')
        loaded.append("Calculator")
    if choose:
        await bot.load_extension('Backend.Modules.choose')
        loaded.append("Choose")
    if perms:
        await bot.load_extension('Backend.Modules.perms')
        loaded.append("Perms")
    if snipe:
        await bot.load_extension('Backend.Modules.snipe')
        loaded.append("Snipe")
    if music:
        await bot.load_extension('Backend.Modules.music')
        loaded.append("Music")
    if avatar:
        await bot.load_extension('Backend.Modules.avatar')
        loaded.append("Avatar")
    if quote:
        await bot.load_extension('Backend.Modules.quote')
        loaded.append("Quote")
    if ollama:
        await bot.load_extension('Backend.Modules.ollama')
        loaded.append("Ollama")
    if reverse:
        await bot.load_extension('Backend.Modules.reverse')
        loaded.append("Reverse")
    if dictionary:    
        await bot.load_extension('Backend.Modules.dictionary')
        loaded.append("Dictionary")
    if afk:
        await bot.load_extension('Backend.Modules.afk')
        loaded.append("Afk")
    if qotd:
        await bot.load_extension('Backend.Modules.qotd')
        loaded.append("Qotd")
    if lyrics:
        await bot.load_extension('Backend.Modules.lyrics')
        loaded.append("Lyrics")
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
    if help:
        await bot.load_extension('Backend.Modules.help')
        loaded.append("Help")
    print("--------------------------------")
    print(f"Cogs loaded: {', '.join(loaded)}")
    print("--------------------------------")
