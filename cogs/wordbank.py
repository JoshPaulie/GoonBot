"""
TODO Create func, define term, add
TODO Multiple definitions with authors, per word
"""
from discord.ext import commands


class WordBank(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None


def setup(bot):
    bot.add_cog(WordBank(bot))
