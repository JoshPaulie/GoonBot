import discord
from discord.ext import commands
from bot_config import joshpaulie
from modules.paulie_tools import color_range, error_embed


class SuggestionBox(commands.Cog, name="Suggestion Box 📝"):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="suggestions", aliases=['requests'])
    async def suggestions(self, ctx):
        """Display a list of community suggestions"""
        embed = discord.Embed(title="Community Suggestions!")
        suggestion_count = 0
        async for suggestion in self.bot.suggestions.find():
            embed.add_field(name=suggestion['author'],
                            value=suggestion['suggestion'],
                            inline=False)
            suggestion_count += 1
        embed.description = f"Suggestion count: {suggestion_count}"
        embed.colour = discord.Colour.from_rgb(color_range(), color_range(), color_range())
        await ctx.send(embed=embed)

    @commands.command(name="suggestion", aliases=['request', 'suggest', 'demand'])
    async def suggestion(self, ctx, *, suggestion):
        """Make a suggestion for Goonbot!"""
        josh = self.bot.get_user(joshpaulie)
        suggestion_form = {"author": ctx.author.name, "suggestion": suggestion}
        await self.bot.suggestions.insert_one(suggestion_form)
        embed = discord.Embed(title="Suggestion submitted!",
                              description=f'*"{suggestion}"*')
        embed.colour = discord.Colour.from_rgb(color_range(), color_range(), color_range())
        await ctx.send(embed=embed)
        await josh.send(f"*{ctx.author.name}* suggests **{suggestion}**")

    @suggestion.error
    async def suggestion_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await error_embed(ctx, "You didn't suggest anything! Goofball!")


def setup(bot):
    bot.add_cog(SuggestionBox(bot))
