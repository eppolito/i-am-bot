################################# Discord Bot! #################################
from nextcord import Interaction, ChannelType #, SlashOption
# from nextcord.abc import GuildChannel
from nextcord.ext import commands
import nextcord
import re, os, datetime
import requests, json
import asyncio
from dotenv import load_dotenv

############################### Setup Environment ##############################

# parameter for turning testing on/off easily
is_test = True

# load our environment
load_dotenv()
# token for bot
TOKEN = os.getenv("TOKEN")
# vip ids for the bot
owner_id = int(os.getenv("owner_id"))
admin_ids = [owner_id]

# handling for dnd announcements
dnd_date = datetime.datetime(
    year=int(os.getenv("dnd_year")),
    month=int(os.getenv("dnd_month")),
    day=int(os.getenv("dnd_day")),
    hour=8,
    minute=0,
    second=0
)
dnd_delta = datetime.timedelta(days=14)
# key for the chuck norris api
norris_key = os.getenv("norris_key")

# IDs for the bot to use
if is_test:
    bot_channel = int(os.getenv("test_bot_channel"))
    dnd_channel = int(os.getenv("test_bot_channel"))
    guild_id = int(os.getenv("test_guild_id"))
else:
    bot_channel = int(os.getenv("live_bot_channel"))
    dnd_channel = int(os.getenv("live_dnd_channel"))
    guild_id = int(os.getenv("live_guild_id"))


############################ General Use Functions #############################

# regex for matching a word in string regardless of case
has_word = lambda w, s: re.compile(f'.*{w}.*', re.IGNORECASE).match(s)

# comment on os
async def os_comments(message):
    '''make comments on various operating systems'''
    user_message = str(message.content)
    if has_word("linux", user_message):
        await message.reply("Linux is the one true operating system!")
    if has_word("windows", user_message):
        await message.reply("I'm sorry to hear your computer has a virus...  You said it has Windows, right?")
    if has_word("mac([^a-z]|$)", user_message) or has_word("iphone", user_message):
        await message.reply("Are you planning to buy the new iPhone that's coming out with the (slightly) bigger camera and longer charging cable?")
    return

# scheduled messages
async def scheduled_message(
        bot,
        message,
        final_message,
        announce_delta,
        announce_first=None,
        announce_end=None,
        channel=bot_channel
):
    '''repeat sending a message'''
    now = datetime.datetime.utcnow()
    if announce_first == None:
        announce_first = datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
        pass
    if announce_end == None or any((y - x).total_seconds() < 0 for (x, y) in \
           [(now, announce_first), (announce_first, announce_end), (now, announce_end)]):
        print(f"{datetime.datetime.utcnow()} Malformed scheduled_message cancelled...")
        return
    announce_delta = announce_delta.total_seconds()
    channel = bot.get_channel(channel)
    wait_time = (announce_first - now).total_seconds()
    time_remaining = announce_end - now
    while time_remaining.total_seconds() >= announce_delta + 1:
        await asyncio.sleep(wait_time)
        now = datetime.datetime.utcnow()
        time_remaining = announce_end - now
        wait_time = announce_delta
        print(f"{now} Sending a scheduled message.")
        await channel.send(message.format(time_remaining))
        continue
    wait_time = time_remaining.total_seconds()
    if wait_time > 0:
        await asyncio.sleep(wait_time)
        pass
    await channel.send(final_message)
    return

############################ Basic Bot Functionality ###########################

class Basic(commands.Cog):
    '''The basic setup for the bot, including event listeners.'''

    def __init__(self, bot, channel):
        self.bot = bot
        self.channel = channel
        self.start_time = datetime.datetime.utcnow()
        return

    # do stuff when bot comes online
    @commands.Cog.listener()
    async def on_ready(self):
        '''Stuff to do once the bot comes online'''
        self.online_time = datetime.datetime.utcnow()
        # log bot interaction
        print(f"{datetime.datetime.utcnow()} Logged in as {str(self.bot.user)}.")
        # announce bot has come online
        await self.bot.get_channel(self.channel).send("`i_am_bot.py` raised an Exception.  Traceback (line 66, column 6): `I... feel... alive...`")
        await scheduled_message(
            self.bot,
            "DnD is coming!  Time remaining is {}.",
            "DnD is here!",
            dnd_delta,
            announce_end=dnd_date,
            channel=dnd_channel
        )
        return

    # when messages received
    @commands.Cog.listener()
    async def on_message(self, message):
        '''How to handle messages'''
        # log messages from the server
        print(f"{str(message.created_at)} {message.author} ({str(message.channel.name)}): {repr(message.content)}")
        # prevent infinite loops
        if message.author == self.bot.user:
            return
        # comment on operating systems
        await os_comments(message)
        return

    @commands.Cog.listener()
    async def on_error(self, error, *args, **kwargs):
        '''How to handle errors'''
        error_message = '\n'.join((error,) + args + kwargs)
        await self.bot.get_channel(self.channel).send(f"I have encountered an error that I don't understand:\n{error}")
        os.write(2, error_message)
        return

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        '''How to process errors from user commands'''
        await ctx.message.reply(f"Something has gone wrong...  Try `$help` for information about commands I know.")
        print(f"{datetime.datetime.utcnow()} {str(error)}")
        return

    @commands.command(
        name="stats",
        description="Get basic information about the bot.",
        guild_ids=[guild_id]
    )
    async def stats(self, ctx : Interaction):
        '''Print basic stats about the bot'''
        uptime = datetime.datetime.utcnow() - self.start_time
        online = datetime.datetime.utcnow() - self.online_time
        # cpu = psutil.cpu_percent()
        # ram = psutil.virtual_memory()[2]
        # await self.bot.get_channel(bot_channel).send(f"```Uptime: {uptime}\nOnline: {online}\nCPU:    {cpu}%\nRAM:    {ram}%```")
        await self.bot.get_channel(bot_channel).send(f"```Uptime: {uptime}\nOnline: {online}```")
        return

    pass

bot = commands.Bot(command_prefix='$')
bot.add_cog(Basic(bot, bot_channel))
bot.run(TOKEN)
