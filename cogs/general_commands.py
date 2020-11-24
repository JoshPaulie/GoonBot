import random
import discord
import asyncio
from discord.ext import commands
from pathlib import Path

files_assets_path = Path("helpers")


class GeneralCommands(commands.Cog, name="General ⚙"):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='suggestion', aliases=['suggest', 'request'])
    async def suggestion(self, ctx, *, command_suggestion):
        """Logs a suggestions and requests in notepad file, with username"""
        message = ctx.message
        with open(files_assets_path / 'suggestions.txt', mode='a') as file:
            file.write(f'- {command_suggestion}, {message.author.name}\n')
        await ctx.send(f'Suggestion submitted, thanks *{message.author.name}*!')

    @commands.command(name='suggestions', aliases=['requests'])
    async def suggestions(self, ctx):
        """Displays list of all submitted suggestions, lol"""
        with open(Path(files_assets_path / 'suggestions.txt'), mode='r') as file:
            await ctx.send(f'```\n'
                           f'Current suggestions:\n'
                           f'{file.read()}\n'
                           f'```')

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
    async def coinflip(self, ctx, tosses: int = 1):
        """Coinflip! Add a number after for multiple tosses =]"""
        message = ctx.message

        def coinflip():
            coin = random.randint(0, 1)
            if coin:
                return f'**Heads!** `{coin}`'
            return f'**Tails!** `{coin}`'

        if tosses < 11:
            for x in range(tosses):
                await ctx.send(f'{coinflip()}')
        else:
            await ctx.send('You can\'t toss more than 10 at a time.')

    @commands.command(name='vtuber', aliases=['vtubers', 'vtube'])
    async def vtuber(self, ctx):
        """A long awaited feature"""
        message = ctx.message
        emojis = ['🤫', '😉']
        await message.delete()
        shush_msg = await ctx.send(random.choice(emojis))
        await asyncio.sleep(1)
        await shush_msg.delete()


def setup(bot):
    bot.add_cog(GeneralCommands(bot))
