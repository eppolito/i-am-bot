from setup import *


################################# Fun Commands #################################

class Fun(commands.Cog):
    '''Fun commands :)'''

    def __init__(self, bot):
        self.bot = bot
        return

    # inspirational quotes
    @commands.command(
        name="inspire",
        description="Produce a random inspirational quote from the Zenquotes API.",
        scope=guild_id
    )
    async def inspire(self, ctx : Interaction):
        '''Random inspirational quote'''
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q']
        author = json_data[0]['a']
        quote_with_attribution = f'{quote}  --{author}'
        await ctx.send(quote_with_attribution)
        return

    # random chuck norris fact
    @commands.command(
        name="norris",
        description="Produce a random fact about the great Chuck Norris from the chuck-norris-jokes API.",
        scope=guild_id
    )
    async def norris(self, ctx : Interaction):
        '''Random Chuck Norris fact'''
        headers = {
	    "accept": "application/json",
	    "X-RapidAPI-Host": "matchilling-chuck-norris-jokes-v1.p.rapidapi.com",
	    "X-RapidAPI-Key": norris_key
        }
        response = requests.request("GET", "https://matchilling-chuck-norris-jokes-v1.p.rapidapi.com/jokes/random", headers=headers)
        json_data = json.loads(response.text)
        quote = json_data["value"]
        await ctx.send(quote)
        return

    pass
