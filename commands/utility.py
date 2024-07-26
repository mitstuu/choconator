import discord
import datetime
import asyncio
import json
import os
import calendar

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


## BIRTHDAYS FEATURE


# "birthdays" global dictionary to store the birthdays data
global birthdays
birthdays = {}



# save_data function to save the birthdays data
def save_data():
    os.makedirs('data', exist_ok=True) # Create a 'data' directory if it doesn't exist
    with open('data/birthdays.json', 'w') as f:
        json.dump(birthdays, f, indent=4)

# load_data function to load the birthdays data
def load_data():
    global birthdays
    with open('data/birthdays.json', 'r') as f:
        data = json.load(f)
        birthdays = data.get('birthdays', {})


# command to set a user's birthday
async def birthday(ctx, month: int, day: int):
    """
    Set your birthday. Example: c.bday 1 1 (for January 1st)
    :param day: The day of your birthday.
    :param month: The month of your birthday.
    """
    user_id = ctx.author.id
    if ctx.channel.id == 817123974147473478:
        if user_id not in birthdays:
            birthdays[user_id] = {}
        birthdays[user_id]['day'] = day
        birthdays[user_id]['month'] = month

        save_data()

        month_name = calendar.month_name[month]
        await ctx.reply(f'{ctx.author.display_name}: 🎂 Noted, I will wish you a happy birthday on __**{month_name} {day}**__!')
    else:
        return


# loop task function to check for birthdays
async def check_birthdays(bot):
    today = datetime.date.today()
    birthday_channel = bot.get_channel(877933827320856596)
    birthdays = load_data()
    for user_id, data in birthdays.items():
        if today.month == data['month'] and today.day == data['day']:
            user = await bot.fetch_user(user_id)
            await birthday_channel.send(f"Today is {user.mention}'s birthday! Happy birthday! 🎉")


# before_loop function for the loop task
async def before_check_birthdays(bot):
    await bot.wait_until_ready()  # Wait until the bot logs in
    now = datetime.datetime.now()
    next_run = now.replace(hour=0, minute=0, second=0) + datetime.timedelta(days=1)  # Next run at 00:00
    sleep_time = (next_run - now).total_seconds()
    await asyncio.sleep(sleep_time)  # Sleep until it's time for the next run