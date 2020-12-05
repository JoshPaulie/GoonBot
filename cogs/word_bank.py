import discord
from discord.ext import commands

from modules.paulie_tools import color_range


class WordBank(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="wordbank")
    async def wordbank(self, ctx):
        """Prints list of all the terms and phrases saved in the word bank"""

    @commands.command(name="define")
    async def define(self, ctx, term):
        """Testing out wait for"""
        embed = discord.Embed(title="Definition Wizard 🧙‍♂️", description=f"What does **{term}** mean?")
        embed.colour = discord.Colour.from_rgb(color_range(), color_range(), color_range())

        def response_check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        prompt = await ctx.send(embed=embed)

        meaning = await self.bot.wait_for('message', check=response_check)
        await meaning.delete()
        embed.description = f"*{meaning.content}*"
        embed.title = term
        embed.set_footer(text="Definition was added to the word bank!\n"
                              "(Not really, this was a POC")
        embed.colour = discord.Colour.from_rgb(color_range(), color_range(), color_range())
        await prompt.edit(embed=embed)



def setup(bot):
    bot.add_cog(WordBank(bot))
