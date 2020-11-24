from discord.ext import commands


class Links(commands.Cog, name="Links! 🌐"):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='paypig', aliases=['dekar'])
    async def paypig(self, ctx):
        """Link to Dekar's stream"""
        message = ctx.message
        await ctx.send('https://www.twitch.tv/dekar173')
        await message.add_reaction('🐽')

    @commands.command(name='jerma', aliases=['jerma985'])
    async def github(self, ctx):
        """Link to Jerma's Stream"""
        await ctx.send('https://www.twitch.tv/jerma985')


def setup(bot):
    bot.add_cog(Links(bot))
