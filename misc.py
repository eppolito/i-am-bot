############################ General Use Functions #############################
from setup import *

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

# TODO: make this a bit more database friendly...
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
    now = datetime.utcnow()
    if announce_first == None:
        announce_first = datetime.utcnow() + timedelta(minutes=1)
        pass
    if announce_end == None or any((y - x).total_seconds() < 0 for (x, y) in \
           [(now, announce_first), (announce_first, announce_end), (now, announce_end)]):
        print(f"{datetime.utcnow()} Malformed scheduled_message cancelled...")
        return
    announce_delta = announce_delta.total_seconds()
    channel = bot.get_channel(channel)
    wait_time = (announce_first - now).total_seconds()
    time_remaining = announce_end - now
    while time_remaining.total_seconds() >= announce_delta + 1:
        await asyncio.sleep(wait_time)
        now = datetime.utcnow()
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
