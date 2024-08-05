import discord
from discord.ext import commands

class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Add your commands here

def setup(bot):
    bot.add_cog(UserCommands(bot))

@commands.command()
@commands.cooldown(1, 1800, commands.BucketType.guild)
async def revivechat(self, ctx):
    channel_id = 123456789  # Replace with the desired channel ID
    if ctx.channel.id == channel_id:
        await ctx.send('Stop touching grass and chat with us! @mitstuu (replace with reviver ping)')
    else:
        await ctx.send('This command can only be used in the specified channel.')
