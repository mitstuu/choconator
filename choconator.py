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
CHOCONATOR_TOKEN = os.getenv('CHOCONATOR_TOKEN')
if CHOCONATOR_TOKEN is None:
    print("Error: CHOCONATOR_TOKEN environment variable is not set.")
    exit(1)

# bot instance
bot= commands.Bot(
        command_prefix='c.',
        intents=intents,
        application_id=1265797492109479977,
  )  

# load cogs
cog_directory = 'cogs'
async def load_cogs():
    for filename in os.listdir(cog_directory):
        if filename.endswith('.py') and not filename.startswith('__'):
            cog_name = filename[:-3]  # Remove the .py extension
            try:
                module = importlib.import_module(f'{cog_directory}.{cog_name}')
                if hasattr(module, 'setup'):
                    await module.setup(bot)
                print(f'Successfully loaded cog: {cog_name}')
            except Exception as e:
                print(f'Failed to load cog {cog_name}: {e}')

## events

# check if bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id}), app ID: {bot.application_id}")
    # List all guilds your bot is in
    print("Guilds available to bot:", [(g.name, g.id) for g in bot.guilds])

    # Show what commands the tree currently knows about
    cmds_before = [c.name for c in bot.tree.get_commands()]
    print("Commands before sync:", cmds_before)

    # (Optional) clear stale commands on that guild first
    guild_obj = discord.Object(id=775209879921098792)
    print("Attempting to clear commands in test guild")
    try:
        bot.tree.clear_commands(guild=guild_obj)
        print("Cleared commands in test guild")
    except Exception as e:
        print("Error during clear_commands:", repr(e))

    print("Attempting to sync commands in test guild")
    try:
        synced = await bot.tree.sync(guild=guild_obj)
        print("Synced these commands to guild:", [c.name for c in synced])
    except Exception as e:
        print("Error during sync:", repr(e))

    print("Checking commands after sync")
    try:
        cmds_after = [c.name for c in bot.tree.get_commands()]
        print("Commands after sync:", cmds_after)
    except Exception as e:
        print("Error getting commands after sync:", repr(e))

# event for disconnecting
@bot.event
async def on_disconnect():
    print('Choconator has disconnected from Discord!')


# run the bot

async def main():
    # Load all cogs before connecting so Cog listeners register in time
    await load_cogs()
    await bot.start(CHOCONATOR_TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())