from setup import *

# random die rolls
roll = lambda k, n: tuple(randint(1, n) for i in range(k))
roll_regexp = "^(([1-9][0-9]?)d([1-9][0-9]?)(([\\+\\-])([1-9][0-9]?))?|adv|dis)$"

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

Takes multiple arguments of the form <k>d<n> to roll k n-sided dice.
Also parses advantage and disadvantage rolls as arguments <adv> and <dis>.

Arguments must match the following regular expression.
      ^(([1-9][0-9]?)d([1-9][0-9]?)(([\\+\\-])([1-9][0-9]?))?|adv|dis)$
Thus this function ignores all arguments greater than 99 (for Rhizka-proofing).
'''
        regex = re.compile(roll_regexp)
        ans = []
        pad_num = 3
        for arg in args:
            my_roll = regex.match(arg)
            pad_num = max(pad_num, len(arg))
            if not my_roll:
                continue
            [r, k, n, e, o, m] = my_roll.groups()
            if r == "adv":
                adv = roll(2, 20)
                ans.append((arg, f"{max(adv)} = max{adv}"))
            elif r == "dis":
                dis = roll(2, 20)
                ans.append((arg, f"{min(dis)} = min{dis}"))
            else:
                my_roll = roll(int(k), int(n))
                tot = sum(my_roll)
                if o == "+":
                    tot += int(m)
                elif o == "-":
                    tot -= int(m)
                else:
                    e = ""
                    pass
                ans.append((arg, f"{tot} = sum{my_roll}{e}"))
                continue
            continue
        ans_string = ""
        for (arg, st) in ans:
            pad = ' '*(pad_num - len(arg))
            ans_string += f"{arg}:{pad} {st}\n"
            continue
        if bool(ans_string):
            await ctx.send(f"```\n{ans_string}```")
            return
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
