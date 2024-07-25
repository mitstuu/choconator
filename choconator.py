import discord
from discord.ext import commands
import os


# Use environment variables to define CHOCONATOR_TOKEN
CHOCONATOR_TOKEN = os.environ.get('CHOCONATOR_TOKEN')

if CHOCONATOR_TOKEN is None:
    print("Error: CHOCONATOR_TOKEN environment variable is not set.")
    exit(1)

# Create an instance of the bot
bot = commands.Bot(command_prefix='c.')

# Load all the cogs
cogs = ['cogs.admin', 'cogs.moderation']  # Add more cogs here if needed

for cog in cogs:
    try:
        bot.load_extension(cog)
        print(f"Loaded {cog} cog successfully.")
    except Exception as e:
        print(f"Failed to load {cog} cog. Error: {e}")

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

# Run the bot
bot.run('CHOCONATOR_TOKEN')