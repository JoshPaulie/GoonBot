import discord
from discord.ext import commands


class Links(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='paypig', aliases=['dekar'])
    async def paypig(self, ctx):
        '''Link to Dekar's stream'''
        message = ctx.message
        await ctx.send('https://www.twitch.tv/dekar173')
        await message.add_reaction('🐽')

    @commands.command(name='github', aliases=['code', 'source'])
    async def github(self, ctx):
        '''Check out the python code 🐍'''
        await ctx.send('https://github.com/JoshPaulie/GoonBot')

    @commands.command(name='jerma', aliases=['jerma985'])
    async def github(self, ctx):
        '''Link to Jerma'''
        await ctx.send('https://www.twitch.tv/jerma985')


def setup(bot):
    bot.add_cog(Links(bot))
