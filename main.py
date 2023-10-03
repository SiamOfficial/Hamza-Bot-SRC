import discord
from discord.ext import commands
import asyncio
import os
import time
import asqlite
import threading

# Discord Bot Code

intents = discord.Intents.default()
intents.guilds = True
bot = commands.Bot(command_prefix='$$', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'Signed in as {bot.user}')
    await bot.tree.sync()
    print(bot.guilds)

@bot.listen('on_message')
async def messaging(message):
    await bot.process_commands(message)

async def main():
    for filename in os.listdir('./cogs/commands'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.commands.{filename[:-3]}')
    for filename in os.listdir('./cogs/events'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.events.{filename[:-3]}')
    await bot.start("TOKEN HERE")

discord.utils.setup_logging()
asyncio.run(main)