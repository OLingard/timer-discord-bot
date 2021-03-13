from os import getenv

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')

intents = discord.Intents(messages=True)

bot = commands.Bot(command_prefix=">>", intents=intents)

bot.load_extension('start.start_cog')
# bot.load_extension('stop_timer')
# bot.load_extension('repeat_timer')

bot.run(TOKEN, bot=True, reconnect=True)
