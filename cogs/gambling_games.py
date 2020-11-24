import discord
import random
from modules.sql_helper import *
from discord.ext import commands
from pathlib import Path

files_assets_path = Path("helpers")

possible_scratches = ['🍎', '🥭', '🍌', '🍒', '🍑']


def purchase_check(current_balance, costofitem):
    if current_balance < costofitem:
        return False
    else:
        return True


def rScratchbox():
    return random.choice(possible_scratches)


def play_scratchoff():
    scratch_sheet = [rScratchbox(), rScratchbox(), rScratchbox()]

    if scratch_sheet[0] == scratch_sheet[1] == scratch_sheet[2]:
        return 4, scratch_sheet
    elif scratch_sheet[0] == scratch_sheet[1] or scratch_sheet[1] == scratch_sheet[2]:
        return 2, scratch_sheet
    else:
        return 0, scratch_sheet


class Scratchers(commands.Cog, name="Gambling Games! 🎲"):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name='s3', aliases=['scratcher', 'scratchoff'])
    async def scratchoff(self, ctx):
        """Plays 1 scratch off"""
        message = ctx.message

        data = query(ctx.author.id)
        current_money = data[1]

        if purchase_check(current_money, 1):
            change_money(ctx.author.id, -1)
            sheet = play_scratchoff()
            winnings = sheet[0]
            slot1, slot2, slot3 = sheet[1]

            embed = discord.Embed(title='You bought a 3 Slot Scratcher!', description='3 of a kind or 2 in a row!')
            embed.add_field(name='Sheet', value=f'||{slot1}|| ||{slot2}|| ||{slot3}||', inline=True)
            embed.add_field(name='Winnings', value=f'||{winnings}||', inline=True)
            await ctx.send(embed=embed)
            if winnings > 0:
                change_money(ctx.author.id, winnings)
        else:
            await ctx.send("You don't have enough BORB to buy a scratcher!")


def setup(bot):
    bot.add_cog(Scratchers(bot))
