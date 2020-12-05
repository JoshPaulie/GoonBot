from discord.ext import commands


class DevRoom(commands.Cog, name="Dev room! ⚠"):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None


def setup(bot):
    bot.add_cog(DevRoom(bot))
