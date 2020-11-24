import discord
import random
import datetime
from discord.ext import commands
from pathlib import Path

files_assets_path = Path("helpers")


class hobousernames(commands.Cog, name="Hobo's Usernames! 🤖"):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.cooldown(1, 5)
    @commands.command(name='username', aliases=['hobo', 'un', 'name'])
    async def username(self, ctx):
        """Fetches one of Hobo's Signature Usernames"""

        if datetime.datetime.now().month == 11:

            with open(Path(files_assets_path / 'hobo_usernames/hobo_usernames.txt')) as file:
                random_name = random.choice(file.readlines())
            await ctx.send(random_name)
        else:
            with open(Path(files_assets_path / 'hobo_usernames/hobo_halloween_usernames.txt')) as file:
                random_name = random.choice(file.readlines())
            await ctx.send(random_name)

    @username.error
    async def usernameError(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"Hey there! **To prevent repeats and ensure a positive user experience**, you must wait `{round(error.retry_after)}` more seconds.")

    @commands.command(name='addnames')
    async def howaddnames(self, ctx):
        """Instructions on how Hobo can add more names"""
        message = ctx.message
        with open(files_assets_path / 'how_to_add_names.txt', mode='r') as instructions:
            read_inst = instructions.read()
            await message.author.send(read_inst)

    @commands.command(name='howmany', aliases=['howmanynames', 'howmanyusernames'])
    async def howmanynames(self, ctx):
        """Lets you know how many names are on Hobo's growing list"""
        with open(files_assets_path / 'hobo_usernames.txt', mode='r') as file:
            for i, l in enumerate(file):
                pass
            amount_of_names = i + 1
        await ctx.send(f'There are currently `{amount_of_names}` entries in Hobo\'s growing list of names.')

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.DMChannel) and message.author.id == 104489704308604928:
            with open(files_assets_path / 'hobo_usernames.txt', mode='a') as file:
                file.write(f'{message.content}\n')


def setup(bot):
    bot.add_cog(hobousernames(bot))
