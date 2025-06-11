import discord
from discord.ext import commands
import math

class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Add your commands here


    @commands.hybrid_command(name="revivechat", description="Revive chat in the main channel")
    @commands.cooldown(1, 1800, commands.BucketType.guild)
    @commands.guild_only()
    async def revivechat(self, ctx: commands.Context):
        channel_id = 820784545426964480  # Replace with the desired channel ID
        if ctx.channel.id == channel_id:
            await ctx.send('Stop touching grass and chat with us! @mitstuu (replace with reviver ping)')
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
    await bot.tree.sync()