import discord
import datetime
import asyncio
import json

# event function for when a member joins the server
async def on_member_join(member):
    # Check if the member is indeed a new member, joining for the first time
    if member.joined_at is None:
        # welcome card in welcome channel
        channel = discord.utils.get(member.guild.text_channels, id=775210285853835265)
        rules_channel = discord.utils.get(member.guild.text_channels, id=775210186364813372)
        embed = discord.Embed(title=f'Welcome to Choco Bar, {member.mention}!', description=f'Please read the {rules_channel.mention}, and we hope you enjoy your stay!', color=0xd95455)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f'Joined at {datetime.datetime.now()}')
        await channel.send(embed=embed)

        # welcome message in general chat
        channel = discord.utils.get(member.guild.text_channels, id=820784545426964480)
        welcomers = discord.utils.get(member.guild.roles, id= 880797572166467644)
        await channel.send(f'Welcome to Choco Bar, {member.mention}! {welcomers.mention}s, assemble!')


## BIRTHDAYS FEATURE


# "birthdays" global dictionary to store the birthdays data
global birthdays
birthdays = {}



# save_data function to save the birthdays data
def save_data():
    with open('data/birthdays.json', 'w') as f:
        json.dump(birthdays, f, indent=4)

# load_data function to load the birthdays data
def load_data():
    global birthdays
    with open('data/birthdays.json', 'r') as f:
        data = json.load(f)
        birthdays = data.get('birthdays', {})


# command to set a user's birthday
async def birthday(ctx, day: int, month: int):
    """
    Set your birthday.
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

        await ctx.respond(f'{ctx.author.display_name}: Noted, I will wish you happy birthday on {month}/{day}!')
    else:
        return


# loop task function to check for birthdays
async def check_birthdays(bot):
    today = datetime.date.today()
    birthday_channel = bot.get_channel(817123974147473478)
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