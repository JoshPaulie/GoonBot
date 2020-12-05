import random
from pathlib import Path

import discord
from discord.ext import commands

from modules.paulie_tools import color_range, error_embed

files_assets_path = Path("helpers")


class hobousernames(commands.Cog, name="Hobo's Usernames! 🤖"):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.cooldown(1, 5)
    @commands.command(name='username', aliases=['hobo', 'un', 'name'])
    async def username(self, ctx):
        """Fetches one of Hobo's Signature Usernames"""
        with open(Path('helpers/hobo_usernames/hobo_usernames.txt')) as file:
            random_name = random.choice(file.readlines())
        embed = discord.Embed(title=random_name)
        embed.colour = discord.Colour.from_rgb(color_range(), color_range(), color_range())
        await ctx.send(embed=embed)

    @username.error
    async def usernameError(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await error_embed(ctx, f"Hey there! **To prevent repeats and ensure a positive user experience**, "
                                   f"you must wait {round(error.retry_after)} more second(s)")

    @commands.command(name='howmany', aliases=['howmanynames', 'howmanyusernames'])
    async def howmanynames(self, ctx):
        """Lets you know how many names are on Hobo's growing list"""
        with open('helpers/hobo_usernames/hobo_usernames.txt', mode='r') as file:
            for i, l in enumerate(file):
                pass
            amount_of_names = i + 1
        embed = discord.Embed(title=f"{amount_of_names} hand-crafted", description="*hobo usernames*")
        embed.colour = discord.Colour.from_rgb(color_range(), color_range(), color_range())
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.DMChannel) and message.author.id == 104489704308604928:
            with open(files_assets_path / 'hobo_usernames.txt', mode='a') as file:
                file.write(f'{message.content}\n')


def setup(bot):
    bot.add_cog(hobousernames(bot))
