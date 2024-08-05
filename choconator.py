# Description: Main file for the Choconator bot.

# import libraries
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import importlib

# import cogs
from cogs import *

load_dotenv()

# set intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# environment variables
CHOCONATOR_TOKEN = os.getenv('CHOCODEV_TOKEN')
if CHOCONATOR_TOKEN is None:
    print("Error: CHOCONATOR_TOKEN environment variable is not set.")
    exit(1)

# bot instance
bot = commands.Bot(command_prefix='c.', intents=intents)

# load cogs
# load cogs
cog_directory = 'cogs'
for filename in os.listdir(cog_directory):
    if filename.endswith('.py') and not filename.startswith('__'):
        cog_name = filename[:-3]  # Remove the .py extension
        module = importlib.import_module(f'{cog_directory}.{cog_name}')
        if hasattr(module, 'setup'):
            module.setup(bot)


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