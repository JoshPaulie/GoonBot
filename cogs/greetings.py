from discord.ext import commands
from pathlib import Path

files_assets_path = Path("files_assets")


class Greetings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def hello(self, ctx):
        """Simple greeting"""
        message = ctx.message
        await ctx.send(f'Hey there, {message.author.name}!')
        await message.add_reaction('👋')


def setup(bot):
    bot.add_cog(Greetings(bot))
