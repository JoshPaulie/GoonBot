import datetime
import random

import colored
from colored import stylize
from discord.ext import commands, tasks

from modules.paulie_tools import calc_time, current_time

time_keeper_file = "files_assets/time_keeper.txt"


class ListenersAndEvents(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        with open(time_keeper_file) as f:
            file_text = f.read()  # * time keeper file -> str
            file_time = datetime.datetime.strptime(file_text, '%Y-%m-%d %H:%M:%S.%f')  # * str -> datetime object
            time_diff = datetime.datetime.now() - file_time
            final_diff = calc_time(time_diff.seconds)
        if time_diff.seconds > 60 * 60:  # * print in console if bot was offline longer than an hour
            print(stylize(f" ! Bot was offline for approx. {final_diff}", colored.fg(196)))
        self.time_keeper.start()  # * starts time_keeper task

    @commands.Cog.listener()
    async def on_command(self, ctx):
        """Prints commands to console"""
        message = ctx.message
        content = message.content
        print(
            f"{stylize(current_time(), colored.fg(115))} ({message.author.name}) {content}")

    @tasks.loop(seconds=10.0)
    async def time_keeper(self):
        """Writes current time to time_keeper.txt"""
        with open(time_keeper_file, "w") as f:
            f.write(str(datetime.datetime.now()))

    @commands.Cog.listener()  # Taboo!
    async def on_message(self, message):
        """Justin ellipsis watcher 👀"""
        condemnings = [
            "You have disappointed Justin.",
            "..Justin is speechless..you should be ashamed.",
            "..."
        ]
        if message.author.id == 104488534936666112 and message.content in ["." * count for count in range(1, 5)]:
            await message.channel.send(random.choice(condemnings))


def setup(bot):
    bot.add_cog(ListenersAndEvents(bot))
