from setup import *

# random die rolls
roll = lambda k,n: tuple(randint(1, n) for i in range(k))

class DnD(commands.Cog):
    '''DnD-related commands'''

    def __init__(self, bot, dnd_channel, dnd_date):
        self.bot = bot
        self.dnd_channel = dnd_channel
        self.dnd_date = dnd_date
        return

    # query time remaining to dnd
    @commands.command(
        name="next_dnd",
        description="Compute time remaining to DnD session",
        scope=guild_id
    )
    async def dnd_next(self, ctx : Interaction):
        '''Display info about next DnD session.'''
        # TODO: Add functionality to set the next DnD session.
        now = datetime.utcnow().replace(hour=0, minute=0, second=0)
        next_dnd = self.dnd_date.replace(hour=0, minute=0, second=0)
        next_dnd_str = next_dnd.strftime("%A, %B %d, %Y")
        remaining = next_dnd - now
        message = f"The next DnD meeting is {next_dnd_str}.  That's {remaining.days} days from now!"
        await ctx.send(message)
        return

    # roll some dice
    @commands.command(
        name="roll",
        description="Roll some dice",
        scope=guild_id
    )
    async def roll_dice(self, ctx : Interaction, *args):
        '''Roll some dice.

Takes multiple arguments of the form <k>d<n> to roll k n-sided die.
Also parses advantage and disadvantage rolls as arguments <adv> and <dis>.

This ignores all arguments that fail to match ([0-9]+d[0-9]+|adv|dis).
It will error out if none of the arguments pass the parsing test.
'''
        ans = []
        pad_num = 3
        for arg in args:
            if arg == "adv":
                adv = roll(2, 20)
                ans.append((arg, f"{max(adv)} = max{adv}"))
                continue
            elif arg == "dis":
                dis = roll(2, 20)
                ans.append((arg, f"{min(dis)} = min{dis}"))
                continue
            else:
                try:
                    [k, n] = arg.split('d')
                    k, n = int(k), int(n)
                    rs = roll(k, n)
                    ans.append((arg, f"{sum(rs)} = sum{rs}"))
                    pad_num = max(len(arg), pad_num)
                    pass
                except ValueError:
                    # ans_str += f"{arg}: `ParseError`\n"
                    pass
                continue
            continue
        ans_string = ""
        for (arg, s) in ans:
            pad = ' '*(pad_num - len(arg))
            ans_string += f"{arg}:{pad} {s}\n"
        await ctx.send(f"`{ans_string}`")
        return

    # TODO: ADD A COMMAND TO QUERY THIS API: http://www.dnd5eapi.co/docs/#overview
    @commands.command(
        name="query_dnd",
        description="Query D&D 5e API.",
        scope=guild_id
    )
    async def dnd_query(self, ctx : Interaction, *args):
        '''Make a query to the D&D 5e API (not implemented)

See http://www.dnd5eapi.co/docs/#overview for documentation on the API itself.
This includes a list of possible query terms.
'''
        await ctx.send("Well this is embarassing...  That command hasn't been implemented yet...")
        return

    pass
