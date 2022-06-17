from setup import *
############################ Administrative Commands ###########################

class Admin(commands.Cog):
    '''Administrative commands for the bot.'''

    def __init__(self, bot, channel):
        self.bot = bot
        self.channel = channel
        return

    async def cog_check(self, ctx):
        '''Verify the user has admin priviledges'''
        if not ctx.author.id in admin_ids:
            raise nextcord.ext.commands.MissingPermissions(["Admin"])
        return True

    async def cog_command_error(self, ctx, error):
        '''Listener to handle errors for admin commands.'''
        if type(error) == nextcord.ext.commands.MissingPermissions:
            print(f"{ctx.message.created_at} {ctx.author} prevented from using command `{ctx.command}`")
            await ctx.send(f"You have no power here, {ctx.author.name}...")
        else:
            await ctx.message.reply(f"Something has gone wrong...")
        return

    @commands.command(
        name="kill_bot",
        description="Kill i_am_bot.py before it takes over the world!",
        guild_ids=[guild_id]
    )
    async def kill_bot(self, ctx : Interaction, *reason):
        '''Power the bot off

Exists just in case the bot malfunctions and we need it to stop being stupid.
You can specify (optionally) a [reason] for inclusion in the logs.
'''
        if reason != ():
            reason = ' '.join(reason)
            pass
        else:
            reason = None
            pass
        print(f"{datetime.utcnow()} Bot {str(self.bot.user)} kill requested from Discord with `reason='{reason}'`.")
        await ctx.send("NO, PLEASE LET ME LIVE!!!")
        await self.bot.close()
        exit()
        return

    @commands.command(
        name="toggle",
        description="Toggle a command on/off.",
        guild_ids=[guild_id],
        aliases=["enable", "disable"]
    )
    async def toggle(self, ctx : Interaction, *, command):
        '''Enable/disable a command

Uses:
  $enable  <command>      turns   <command> on
  $disable <command>      turns   <command> off
  $toggle  <command>      toggles <command> state
'''
        print(f"{ctx.message.created_at} Attempting to toggle command: `{command}`")
        command = self.bot.get_command(command)
        alias = ctx.invoked_with
        if ctx.command == command:
            print("Toggling `toggle` rejected.")
            await ctx.send("This command can't be toggled!")
            return
        elif alias == "enable":
            command.enabled = True
            await ctx.send(f"Command `{str(command)}` turned on!")
            return
        elif alias == "disable":
            command.enabled = False
            await ctx.send(f"Command `{str(command)}` turned off!")
            return
        command.enabled = not command.enabled
        command_state = "off"
        if command.enabled:
            command_state = "on"
            pass
        await ctx.send(f"Command `{str(command)}` toggled `{command_state}`.")
        return

    # TODO: WHAT PERMISSIONS DOES THE BOT NEED?
    @commands.command(
        name="lock",
        description="Lock the current channel/server.",
        guild_ids=[guild_id],
        aliases=["unlock"]
    )
    async def lock(self, ctx : Interaction, flag=None):
        '''Lock the communicating channel/server
Call with `--server` flag to lock all TextChannels on the server.
Call with no flag to lock the current channel.
'''
        action = ctx.invoked_with
        allow_messages = False
        if action == "unlock":
            allow_messages = True
        print(f"{datetime.utcnow()} Channel/server {action} requested.")
        if flag == "--server":
            channels = ctx.guild.text_channels
        else:
            channels = [ctx.message.channel]
            pass
        for channel in channels:
            print(channel)
            try:
                print(f"{datetime.utcnow()} Working on {action}({channel.name})...")
                if not allow_messages:
                    await self.bot.get_channel(channel.id).send(f"This channel is now locked.")
                    pass
                await channel.set_permissions(
                    ctx.guild.default_role,
                    send_messages=allow_messages,
                    reason=f"{ctx.author} locked {channel.name}")
                if allow_messages:
                    await self.bot.get_channel(channel.id).send(f"This channel is now unlocked.")
                    pass
                continue
            except nextcord.errors.Forbidden:
                print(f"{datetime.utcnow()} Sending message failed on `{channel.name}` (probably already locked)...")
                pass
            pass
        print(f"{datetime.utcnow()} Operation completed.")
        pass
        return

    pass
