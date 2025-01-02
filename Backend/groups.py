from Backend.bot import bot
@bot.group(invoke_without_command=True, description="Economy commands")
async def eco(ctx, *args):
    """Economy commands"""
    
    if not args:
        await ctx.send("Available commands: work, daily, balance, steal, shop, coinflip, mafia, stripper")
        return
    command_parts = args[0].split(maxsplit=1)
    command_name = command_parts[0].lower()
    print(f"Parsed command name: {command_name}")
    if command_name == "bal":
        command_name = "balance"
    elif command_name == "stripper":
        command_name = "stripper_cmd"
    
    command = eco.get_command(command_name)
    if command:
        print(f"Executing command: {command.name}")
        
        for arg in args:
            if '<@' in arg:
                user_id = int(''.join(filter(str.isdigit, arg)))
                member = ctx.guild.get_member(user_id)
                print(f"Found mention, processing member: {member}")
                await ctx.invoke(command, member)
                return
        
        if len(command_parts) > 1 or len(args) > 1:
            params = command_parts[1] if len(command_parts) > 1 else args[1]
            if command_name == "coinflip":
                params = int(params)
            await ctx.invoke(command, params)
        else:
            await ctx.invoke(command)

@bot.group(invoke_without_command=True)
async def moderation(ctx, *args):
    """Moderation commands"""
    
    if not args:
        await ctx.send("Available commands: Kick, Ban, Mute, Role, Anti-Raid")
        return
    command_parts = args[0].split(maxsplit=1)
    command_name = command_parts[0].lower()
    print(f"Parsed command name: {command_name}")
    
    command = moderation.get_command(command_name)
    if command:
        print(f"Executing command: {command.name}")
        
        for arg in args:
            if '<@' in arg:
                user_id = int(''.join(filter(str.isdigit, arg)))
                member = ctx.guild.get_member(user_id)
                print(f"Found mention, processing member: {member}")
                await ctx.invoke(command, member)
                return
        
        if len(command_parts) > 1 or len(args) > 1:
            params = command_parts[1] if len(command_parts) > 1 else args[1]
            await ctx.invoke(command, params)
        else:
            await ctx.invoke(command)