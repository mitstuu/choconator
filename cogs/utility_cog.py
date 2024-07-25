from commands import utility
from discord.ext import commands

class UtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # welcome messages
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await utility.on_member_join(member)

    # command to set a user's birthday
    @commands.command()
    async def birthday(self, ctx, day: int, month: int):
        """
        Set your birthday.
        :param day: The day of your birthday.
        :param month: The month of your birthday.
        """
        await utility.birthday(ctx, day, month)

    # loop task for birthday checker
    @commands.Cog.listener()
    async def check_birthdays(self):
        await utility.check_birthdays()

    # before_loop function for the loop task
    @commands.Cog.listener()
    async def before_check_birthdays(self):
        await utility.before_check_birthdays()

def setup(bot):
    bot.add_cog(UtilityCog(bot))

