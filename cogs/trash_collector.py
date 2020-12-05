import discord
from discord.ext import commands
from bot_config import goonbot


class TrashCollector(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Checks for emoji adds"""
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = await self.bot.fetch_user(payload.user_id)
        emoji = payload.emoji.name

        if emoji == "🚮" and message.author.id == goonbot and user.id != goonbot:
            await message.delete()


def setup(bot):
    bot.add_cog(TrashCollector(bot))
