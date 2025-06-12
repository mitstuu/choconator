import discord
from discord.ext import commands
import math

# Hardcoded mention string for the reviver role
REVIVER_ROLE_MENTION = "<@&797299435277254676>"  # replace with your actual role ID

class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Revive chat command
    @commands.hybrid_command(name="revivechat", description="Revive chat in the main channel")
    @commands.cooldown(1, 1800, commands.BucketType.guild)
    @commands.guild_only()
    async def revivechat(self, ctx: commands.Context):
        channel_id = 820784545426964480  # Currently #chat in Choco Bar
        if ctx.channel.id == channel_id:
            allowed_mentions = discord.AllowedMentions(roles=True)
            allowed_mentions.roles.add(REVIVER_ROLE_MENTION)  # Add the reviver role mention
            await ctx.send(f"Stop touching grass and chat with us! {REVIVER_ROLE_MENTION}")
        else:
            await ctx.send('This command can only be used in the main chat channel.')

    @revivechat.error
    async def revivechat_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            minutes = math.ceil(error.retry_after / 60)
            await ctx.send(f"Please wait {minutes} minute{'s' if minutes != 1 else ''} before using this command again.")
        else:
            raise error

async def setup(bot):
    cog = UserCommands(bot)
    await bot.add_cog(cog)

    #guild = discord.Object(id=775209879921098792)  # your Choco Bar guild ID
    # await bot.tree.sync(guild=guild)  # Sync the command tree for the specific guild