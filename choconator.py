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

    # Debug: show each command's configured guild_ids
    print("Command guild_ids mapping:", {
        cmd.name: getattr(cmd, "guild_ids", None)
        for cmd in bot.tree.get_commands()
    })

    # Attempt per-guild sync
    guild_obj = discord.Object(id=775209879921098792)
    try:
        synced = await bot.tree.sync(guild=guild_obj)
        print(f"Per-guild sync returned: {[c.name for c in synced]}")
    except Exception as e:
        print("Error during per-guild sync:", e)

    # If nothing was synced per-guild, fall back to global sync
    if not synced:
        try:
            global_synced = await bot.tree.sync()
            print(f"Global sync returned: {[c.name for c in global_synced]}")
        except Exception as e:
            print("Error during global sync:", e)

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