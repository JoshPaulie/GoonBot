import discord
import random
from discord.ext import commands
from pathlib import Path

from discord.ext.commands import BucketType

files_assets_path = Path("files_assets")


def random_passage():
    with open(Path(files_assets_path / '8ballpassages.txt')) as file:
        passage = str(random.choice(file.readlines()))
    return passage


def random_number():
    return random.randint(0, 100)


class Greetings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.cooldown(1, 24, type=BucketType.user)
    @commands.command(name='8ball',aliases=['eightball', 'shouldi'])
    async def eightball(self, ctx, *, question: str = None):
        """Simple greeting"""
        message = ctx.message

        if question is not None:
            if not question.endswith('?'):
                question = question + '?'

        if question is None:
            embed = discord.Embed(title='Goonbot Insight™',description='Goonbot, who is ever knowing, has looked into '
                                                                       'your heart. The answer to your question '
                                                                       'is..', color=0xbae4f2)
        else:
            embed = discord.Embed(title='Goonbot was asked..', description=f'{question}', color=0xbae4f2)
        embed.add_field(name='Response', value=random_passage(), inline=True)
        embed.add_field(name='Confidence',value=f'`{random_number()}`', inline=True)
        await ctx.send(embed=embed)


    @eightball.error
    async def eightballError(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Goonbot must rest.. **{round(error.retry_after)}** seconds 💤\n*With more responses, this time will decrease. The ability for community responses will be added soon.*")

    @commands.command(name='addresponse', aliases=['add8ball', 'add'])
    async def addresponse(self, ctx, *, response: str = None):
        '''Add responses for the shouldi/8ball command. Must be in a dm!'''
        message = ctx.message
        if response is not None:
            if isinstance(message.channel, discord.DMChannel):
                with open(files_assets_path / '8ballpassages.txt', mode='a') as file:
                    file.write(f'{response}\n')
                await ctx.send('Thanks for contributing :)')
            else:
                await ctx.send('DM me this command instead, like you would in a discord channel.\n`.add [response]`')
                await message.delete()

def setup(bot):
    bot.add_cog(Greetings(bot))
