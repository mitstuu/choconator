# Description: Main file for the Choconator bot.

# import libraries
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

# import cogs
from cogs import utility_cog

load_dotenv()

# set intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# environment variables
CHOCONATOR_TOKEN = os.getenv('CHOCONATOR_TOKEN')
if CHOCONATOR_TOKEN is None:
    print("Error: CHOCONATOR_TOKEN environment variable is not set.")
    exit(1)

# bot instance
bot = commands.Bot(command_prefix='c.', intents=intents)

# load cogs
utility_cog.setup(bot)


## events

# check if bot is ready
@bot.event
async def on_ready():
    print('Choconator has connected to Discord!')
    servers = ''
    for guilds in bot.guilds:
        servers += f'{guilds.name}\n'
    print(f'Connected to {len(bot.guilds)} server(s):\n{servers}')
    await bot.change_presence(activity=discord.Game(name='c.help'))


# event for disconnecting
@bot.event
async def on_disconnect():
    print('Choconator has disconnected from Discord!')


# run the bot
bot.run(CHOCONATOR_TOKEN)