import asyncio
import datetime
from pathlib import Path

import discord
from discord.ext import commands
from modules.paulie_tools import error_embed

files_assets_path = Path("helpers")


class Polls(commands.Cog, name="Polls! 🗳"):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def poll(self, ctx, *, question: str):
        """Creates a poll! Poll expires after 5 minutes. After "results" are displayed

        Syntax: `.poll (question)`"""
        message = ctx.message

        close_time = datetime.datetime.now() + datetime.timedelta(minutes=5)

        if not question.endswith("?"):
            question += "?"
        question = question.capitalize()

        # Create poll embed
        embed = discord.Embed(title=question, description=f"{message.author.name} asked a question!")
        embed.set_footer(text=f'Poll closes in 5 minutes! ({close_time.strftime("%I:%M %p")})')
        poll = await ctx.send(embed=embed)  # Sends poll, stored as variable poll

        base_reactions = ['👍', '👎']
        for reaction in base_reactions:
            await poll.add_reaction(reaction)

        # sleeps for 5 minutes, fetches poll again with updated reactions
        await asyncio.sleep(5 * 60)
        results = await ctx.fetch_message(poll.id)

        new_embed = discord.Embed(title=f"{question} [Closed!]", description=f"{message.author.name} asked a question!")
        # iterate over the results.reactions
        for reaction in results.reactions:
            # if the reaction is in base_reaction, subtract one from count
            if reaction.emoji in base_reactions:
                new_embed.add_field(name=f"{reaction.emoji}", value=f"{reaction.count - 1}", inline=True)
            else:
                new_embed.add_field(name=f"{reaction.emoji}", value=f"{reaction.count}", inline=True)

        await poll.delete()
        await ctx.send(embed=new_embed)

    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await error_embed(ctx, "You need to ask a question!")


def setup(bot):
    bot.add_cog(Polls(bot))
