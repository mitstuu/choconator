from commands import utility
from discord.ext import commands, tasks

class UtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_birthdays.start() # start the loop task for birthdays feature

    # welcome messages
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await utility.on_member_join(member)

    # command to set a user's birthday
    @commands.command(name='bday', aliases=['birthday'])
    async def birthday(self, ctx, month: int, day: int):
        """
        Set your birthday. Example: c.bday 1 1 (for January 1st)
        :param day: The day of your birthday.
        :param month: The month of your birthday.
        """
        await utility.birthday(ctx, month, day)

    # loop task for birthday checker
    @tasks.loop(hours=24)
    async def check_birthdays(self):
        await utility.check_birthdays()

    # before_loop function for the loop task
    @check_birthdays.before_loop
    async def before_check_birthdays(self):
        await utility.before_check_birthdays()

def setup(bot):
    bot.add_cog(UtilityCog(bot))

