import random
from pathlib import Path

import discord
from discord.ext import commands
from modules.paulie_tools import color_range

files_assets_path = Path("helpers")


class GeneralCommands(commands.Cog, name="General ⚙"):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='todo')
    async def todo(self, ctx):
        """Displays list of current being worked on features"""
        with open(Path(files_assets_path / 'todo.txt'), mode='r') as file:
            await ctx.send(f'```\n'
                           f'{file.read()}\n'
                           f'```')

    @commands.command(name='pfp', aliases=['pic'])
    async def pfp(self, ctx, user: discord.Member = None):
        """GOON BOT BEATS BONGO 1000:1"""
        user = user or ctx.author
        embed = discord.Embed(description=f'Here\'s the profile picture for, {user.mention} 😊')
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name='coinflip', aliases=['coin', 'flip', 'cf'])
    async def coinflip(self, ctx):
        """Coinflip! =]"""
        message = ctx.message

        def coin_flip():
            c = random.randint(0, 100)
            if c >= 50:
                return f'Heads! ({c})'
            return f'Tails! ({c})'

        coin = coin_flip()
        embed = discord.Embed(title=coin)
        embed.colour = discord.Colour.from_rgb(color_range(), color_range(), color_range())
        await ctx.send(embed=embed)

    @commands.command(name='vtuber', aliases=['vtubers', 'vtube'])
    async def vtuber(self, ctx):
        """A long awaited feature"""
        message = ctx.message
        emojis = ['🤫', '😉']
        await message.delete()
        await ctx.send(random.choice(emojis), delete_after=1)


def setup(bot):
    bot.add_cog(GeneralCommands(bot))
