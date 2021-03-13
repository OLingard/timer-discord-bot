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

    @commands.command(
        name="start",
        brief="Start a Game Timer",
        help="Starts a game timer for the time specified."
    )
    async def start(self, ctx):
        try:
            self.time_type = TimeTypes(ctx.message.content.split()[-1])
        except ValueError:
            raise TimeTypeError()
        try:
            self.time = int(ctx.message.content.split()[-2])
        except ValueError:
            raise TimeError()

        msg = await ctx.channel.send(self.phrase(0))
        await self.looper(msg)

    async def looper(self, msg):
        if self.time_type == TimeTypes.seconds:
            tasks.Loop(self.countdown_loop(msg), seconds=self.time, minutes=0, hours=0, count=self.time/self.increment,
                       reconnect=True, loop=None)
        if self.time_type == TimeTypes.minutes:
            tasks.Loop(self.countdown_loop(msg), seconds=0, minutes=self.time, hours=0, count=self.time/self.increment,
                       reconnect=True, loop=None)
        if self.time_type == TimeTypes.hours:
            tasks.Loop(self.countdown_loop(msg), seconds=0, minutes=self.time, hours=0, count=self.time/self.increment,
                       reconnect=True, loop=None)

    async def countdown_loop(self, msg):
        self.countdown += self.increment
        msg.edit(self.phrase(self.increment * self.countdown))


def setup(bot):
    bot.add_cog(Start(bot))
