'''
Setup imports and variables for bot.py
'''

############################### Necessary Import ###############################
from psutil import cpu_percent, virtual_memory
from dotenv import load_dotenv
import os, sys
import logging
import logging.handlers

from random import randint

from datetime import datetime, timedelta
import re

from nextcord import Interaction, ChannelType
from nextcord.ext import commands
import nextcord
import requests, json
import asyncio

import traceback

# start time
stats = {
    "uptime_start": datetime.utcnow(),
}

############################# Setup Bot Environment ############################

# load our environment
load_dotenv()
# token for bot
TOKEN = os.getenv("TOKEN")
# vip ids for the bot
owner_id = int(os.getenv("owner_id"))
admin_ids = [owner_id]

# parameter for deciding if this is a test
is_test = os.getenv("is_test") != "False"
# this makes it as difficult as possible to start the bot live on accident

# IDs for the bot to use
if is_test:
    bot_channel = int(os.getenv("test_bot_channel"))
    dnd_channel = int(os.getenv("test_bot_channel"))
    guild_id = int(os.getenv("test_guild_id"))
else:
    bot_channel = int(os.getenv("live_bot_channel"))
    dnd_channel = int(os.getenv("live_dnd_channel"))
    guild_id = int(os.getenv("live_guild_id"))

# handling for dnd announcements
dnd_date = datetime(
    year=int(os.getenv("dnd_year")),
    month=int(os.getenv("dnd_month")),
    day=int(os.getenv("dnd_day")),
    hour=8,
    minute=0,
    second=0
)
dnd_delta = timedelta(days=14)

# key for the chuck norris api
norris_key = os.getenv("norris_key")

################################ Set Up Logging ################################
log_time = stats["uptime_start"].strftime("%Y-%m-%d-%H-%M-%S")
bot_file = os.path.realpath(__file__)
bot_dir  = os.path.dirname(bot_file)
log_dir  = f"{bot_dir}/log"
log_name = f"{log_dir}/{log_time}_bot"
# create log directory unless it already exists
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
    pass
