import datetime
import random

import bot_config
import colored
import discord
from colored import stylize
from discord.ext import commands, tasks
from modules.paulie_tools import calc_time, current_time

time_keeper_file = "helpers/time_keeper.txt"


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
        if ctx.author.id != bot_config.joshpaulie:
            message = ctx.message
            content = message.content
            goon = message.author.name
            console_channel = self.bot.get_channel(bot_config.dashboard_channels['console_channel'])

            embed_on_command = discord.Embed(title=goon, description=content)
            embed_on_command.set_footer(text=f'{current_time()}')
            await console_channel.send(embed=embed_on_command)

    @tasks.loop(seconds=10.0)
    async def time_keeper(self):
        """Writes current time to time_keeper.txt"""
        with open(time_keeper_file, "w") as f:
            f.write(str(datetime.datetime.now()))

    @commands.Cog.listener()  # Taboo!
    async def on_message(self, message):
        """Justin ellipsis watcher 👀"""
        condemning_s = [
            "You have disappointed Justin.",
            "..Justin is speechless..you should be ashamed.",
            "..."
        ]
        if message.author.id == 104488534936666112 and message.content in ["." * count for count in range(1, 5)]:
            await message.channel.send(random.choice(condemning_s))


def setup(bot):
    bot.add_cog(ListenersAndEvents(bot))
