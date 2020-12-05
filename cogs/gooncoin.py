import discord
import pymongo
from discord.ext import commands


class Gooncoin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    async def make_account(self, user_id):
        async for person in self.bot.balance.find():
            exists = False
            if person['discord_id'] == user_id:
                exists = True

            if exists is False:
                await self.bot.balances.insert_one({"discord_id": user_id})

    @commands.command(name="create")
    async def create(self, ctx, user: discord.User):
        """starts of new coins"""
        message = ctx.message
        await self.bot.balances.insert_one({"discord_id": user.id})


def setup(bot):
    bot.add_cog(Gooncoin(bot))
