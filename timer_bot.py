import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from errors import TimeTypeError, TimeError

load_dotenv()

intents = discord.Intents(messages=True)

bot = commands.Bot(command_prefix=">>", intents=intents)

bot.load_extension('start.start_cog')
# bot.load_extension('stop_timer')
# bot.load_extension('repeat_timer')


@bot.event
async def on_command_error(ctx, error):
    with open('err.log', 'a') as f:
        if isinstance(error, commands.errors.CommandNotFound):
            f.write(f'Handled CommandNotFound message: {ctx.message.content}\n'
                    f'    Time of error: {ctx.message.created_at}\n'
                    f'    {error}\n')
            await ctx.author.create_dm()
            await ctx.author.dm_channel.send("Command not found")

        elif isinstance(error.original, (TimeError, TimeTypeError)):
            f.write(f'Handled MessageTypeError: {ctx.message.content}\n'
                    f'    Time of error: {ctx.message.created_at}\n'
                    f'    {error}\n')
            await ctx.author.create_dm()
            await ctx.author.dm_channel.send(error.original)
        else:
            raise error

TOKEN = os.environ['DISCORD_TOKEN']

if __name__ == '__main__':
    bot.run(TOKEN)
