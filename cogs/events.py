import discord
from discord.ext import commands

from modules.paulie_tools import color_range


class EventWizard(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="event")
    async def event(self, ctx):
        """wip"""
        embed = discord.Embed(title="Event Wizard 🧙‍♂️",
                              description=f"Welcome to the Event Wizard!\n"
                                          f"What is the **title** for your event?")
        embed.colour = discord.Colour.from_rgb(color_range(), color_range(), color_range())

        def response_check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        prompt = await ctx.send(embed=embed)

        event_name = await self.bot.wait_for('message', check=response_check)
        await event_name.delete()

        embed.description = f"*{event_name.content}*"
        embed.title = term
        embed.set_footer(text="Definition was added to the word bank!\n"
                              "(Not really, this was a POC")
        embed.colour = discord.Colour.from_rgb(color_range(), color_range(), color_range())
        await prompt.edit(embed=embed)


def setup(bot):
    bot.add_cog(EventWizard(bot))
