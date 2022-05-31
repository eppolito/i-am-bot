################################# Discord Bot! #################################
from nextcord.ext import commands
import nextcord
from dotenv import load_dotenv

############################### Setup Environment ##############################

# load our environment
load_dotenv()
# token for bot
TOKEN = os.getenv("TOKEN")
# vip ids for the bot
owner_id = int(os.getenv("owner_id"))
admin_ids = [owner_id]

bot = commands.Bot(command_prefix='$')
bot.run(TOKEN)
