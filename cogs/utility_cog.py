from discord.ext import commands, tasks
import discord
import datetime
import asyncio
import json
import os
import calendar

class UtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_birthdays.start() # start the loop task for birthdays feature

        # event function for when a member joins the server
    async def on_member_join(member):
        # check if the member is not a bot and has no previous join date
        if (not member.bot) and (member.joined_at is None):
            # welcome card in welcome channel
            channel = discord.utils.get(member.guild.text_channels, id=775210285853835265)
            rules_channel = discord.utils.get(member.guild.text_channels, id=775210186364813372)
            embed = discord.Embed(title=f'Welcome to Choco Bar, {member.display_name}!', description=f'Please read the {rules_channel.mention}, and we hope you enjoy your stay!', color=0xd95455)
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_footer(text=f'Joined at {datetime.datetime.now()}')
            await channel.send(embed=embed)

            # welcome message in general chat
            channel = discord.utils.get(member.guild.text_channels, id=820784545426964480)
            welcomers = discord.utils.get(member.guild.roles, id=880797572166467644)
            await channel.send(f'Welcome to Choco Bar, {member.mention}! {welcomers.mention}s, assemble!')

    # ping command to measure response time
    @commands.command(name='ping')
    async def ping(ctx):
        start_time = datetime.datetime.now()
        message = await ctx.reply("Pinging...")
        end_time = datetime.datetime.now()
        response_time = (end_time - start_time).total_seconds() * 1000
        await message.edit(content=f"Pong! Response time: {response_time} ms")

    # command to set a user's birthday
    @commands.command(name='bday', aliases=['birthday'])
    async def birthday(self, ctx, day: int, month: int, year: int = None):
        """
        Set your birthday. Example: c.bday 1 1 (for January 1st)
        :param day: The day of your birthday.
        :param month: The month of your birthday.
        :param year: (optional) The year of your birthday.
        """
        await utility.birthday(ctx, day, month, year)

    # loop task for birthday checker
    @tasks.loop(hours=24)
    async def check_birthdays(self):
        await utility.check_birthdays()

    # before_loop function for the loop task
    @check_birthdays.before_loop
    async def before_check_birthdays(self):
        await utility.before_check_birthdays(self.bot)

async def setup(bot):
    await bot.add_cog(UtilityCog(bot))

