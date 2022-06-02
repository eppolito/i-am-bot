#!/usr/bin/python3
################################# Discord Bot! #################################
from setup import *

from misc import os_comments, scheduled_message

# setup bot
bot = commands.Bot(command_prefix='$')

################################# Bot Settings #################################

@bot.event
async def on_ready():
    '''Stuff to do once the bot comes online'''
    stats["online_start"] = datetime.utcnow()
    # log bot interaction
    print(f"{datetime.utcnow()} Logged in as {str(bot.user)}.") # ERROR HERE
    # announce bot has come online
    await bot.get_channel(bot_channel).send("`i_am_bot.py` encountered an error (line 66, column 6): `I... feel... alive...`")
    await scheduled_message(
        bot,
        "DnD is coming!  Time remaining is {}.",
        "DnD is here!",
        dnd_delta,
        announce_end=dnd_date,
        channel=dnd_channel
    )
    return

@bot.event
async def on_message(message):
    '''How to handle messages'''
    # log messages from the server
    print(f"{str(message.created_at)} {message.author} ({str(message.channel.name)}): {repr(message.content)}")
    # prevent infinite loops
    if message.author == bot.user:
        return
    # process commands
    await bot.process_commands(message)
    # comment on operating systems
    await os_comments(message)
    return

@bot.event
async def on_error(error_method, *args, **kwargs):
    '''How to handle errors'''
    error = repr(sys.exc_info()[1])
    await bot.get_channel(bot_channel).send(f"I'm ignoring an error that I don't understand:\n```In: {error_method}\nkwArgs: {kwargs}\n{error}```")
    return

@bot.event
async def on_command_error(ctx, error):
    '''How to process errors from user commands'''
    await ctx.message.reply(f"`{error}`.\nTry running `$help` for information about my commands.")
    print(f"{datetime.utcnow()} {str(error)}")
    return


################################# Bot Commands #################################

@bot.command(
    name="stats",
    description="Get basic information about the bot's process.",
    guild_ids=[guild_id]
)
async def stats_command(ctx : Interaction, *args):
    '''Print basic stats on the bot

You can query for a specific stat (or list of stats) by passing it (them) as an argument.
These are the arguments I'll respond to (all others will be ignored).

uptime:   how long the bot has been active as a process
online:   how long the bot has been online
cpu:      estimate the percentage of cpu the bot is using
ram:      estimate the percentage of ram the bot is using

Passing no arguments is equivalent to passing all of them once in the order above.
'''
    current_stats = {
        "uptime": datetime.utcnow() - stats["uptime_start"],
        "online": datetime.utcnow() - stats["online_start"],
        "cpu": cpu_percent(),
        "ram": virtual_memory()[2]
    }
    args = {arg:current_stats[arg] for arg in args if arg in current_stats}
    if args == {}:
        args = current_stats
        pass
    newline = '\n'
    response_str = ""
    pad_len = max(len(stat) for stat in args) + 1
    for stat in args:
        stat_str = stat + ':' + ' '*(pad_len - len(stat))
        response_str += f"\n{stat_str} {current_stats[stat]}"
        continue
    await bot.get_channel(bot_channel).send(f"```{response_str.strip(newline)}```")
    return

@bot.command(
    name="ping",
    description="Check if the bot is responding to commands.",
    guild_ids=[guild_id]
)
async def ping(ctx : Interaction):
    '''Ping the bot

If everything is working, the bot should simply respond "Pong!".'''
    await ctx.send("Pong!")
    return


################################### Load Cogs ##################################

from cogs.admin import Admin
bot.add_cog(Admin(bot, bot_channel))

from cogs.dnd import DnD
bot.add_cog(DnD(bot, dnd_channel, dnd_date))

from cogs.fun import Fun
bot.add_cog(Fun(bot))

################################### Run Bot ####################################

bot.run(TOKEN)
