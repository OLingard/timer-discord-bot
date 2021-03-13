import asyncio

import discord
from discord.ext import commands, tasks

from errors import TimeTypeError, TimeError
from start.time_types import TimeTypes


class Start(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.time = 0
        self.time_type = TimeTypes.seconds
        self.increment = 1
        self.countdown = 0

    def phrase(self, time_removal):
        return f"Timer has {self.time - time_removal} {self.time_type.name} left"

    def reset(self):
        self.time = 0
        self.time_type = TimeTypes.seconds
        self.increment = 1

    @commands.command(
        name="start",
        brief="Start a Game Timer",
        help="Starts a game timer for the time specified."
    )
    async def start(self, ctx):
        self.countdown = 0
        self.reset()
        try:
            self.time_type = TimeTypes(ctx.message.content.split()[-1])
        except ValueError:
            raise TimeTypeError()
        try:
            self.time = int(ctx.message.content.split()[-2])
        except ValueError:
            raise TimeError()

        msg = await ctx.send(self.phrase(0))
        await self.looper(msg)

    async def looper(self, msg):
        if self.time_type == TimeTypes.seconds:
            await self.countdown_loop(msg, 1)
        if self.time_type == TimeTypes.minutes:
            await self.countdown_loop(msg, 60)
        if self.time_type == TimeTypes.hours:
            await self.countdown_loop(msg, 3600)

    async def countdown_loop(self, msg: discord.Message, scale):
        while self.increment * self.countdown < self.time:
            self.countdown += self.increment
            await msg.edit(content=self.phrase(self.increment * self.countdown))
            await asyncio.sleep(self.increment * scale)
        await msg.edit(content="Timer Complete!!")


def setup(bot):
    bot.add_cog(Start(bot))
