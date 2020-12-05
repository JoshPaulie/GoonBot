import asyncio

import discord
import random
from modules.sql_helper import *
from discord.ext import commands
from pathlib import Path
from modules.paulie_tools import error_embed

files_assets_path = Path("helpers")


def purchase_check(current_balance, costofitem):
    if current_balance < costofitem:
        return False
    else:
        return True


class GamblingGames(commands.Cog, name="Gambling Games! 🎲"):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name='s3', aliases=['scratcher', 'scratchoff'])
    async def three_box_scratcher(self, ctx):
        """Plays gambling game: 3 Box Scratch Off"""
        data = query(ctx.author.id)
        current_money = data[1]

        scratch_fruit = ['🍎', '🥭', '🍌', '🍒', '🍑']
        scratch_box = lambda: random.choice(scratch_fruit)

        def play_scratcher_three():
            scratch_sheet = [scratch_box(), scratch_box(), scratch_box()]

            if scratch_sheet[0] == scratch_sheet[1] == scratch_sheet[2]:
                return 4, scratch_sheet
            elif scratch_sheet[0] == scratch_sheet[1] or scratch_sheet[1] == scratch_sheet[2]:
                return 2, scratch_sheet
            else:
                return 0, scratch_sheet

        if purchase_check(current_money, 1):
            change_money(ctx.author.id, -1)
            sheet = play_scratcher_three()
            winnings = sheet[0]
            slot1, slot2, slot3 = sheet[1]

            embed = discord.Embed(title='You bought a 3 Slot Scratcher!', description='Straight, or a pair!')
            embed.add_field(name='Sheet', value=f'||{slot1}|| ||{slot2}|| ||{slot3}||', inline=True)
            embed.add_field(name='Winnings', value=f'||{winnings}||', inline=True)
            await ctx.send(embed=embed)
            if winnings > 0:
                change_money(ctx.author.id, winnings)
        else:
            await error_embed(ctx, "You don't have enough BORB to buy a scratcher! 😅\n"
                                   "For help, call *(1-800-522-4700)*")

    @commands.command(name="rps")
    async def rps(self, ctx, wager: int):
        """starts of rock, paper, scissors!"""
        data = query(ctx.author.id)
        current_money = data[1]

        if purchase_check(current_money, wager):
            global user_input
            ''' VARIABLES '''

            rps_emotes = ['🤘', '📃', '✂']

            ''' CREATES GAME MENU, "PROMPT" '''

            embed = discord.Embed(title="Make your choice!")
            prompt = await ctx.send(embed=embed)
            bot_pick = random.choice(['Rock', 'Paper', 'Scissors'])
            embed.description = f"The bot picked {bot_pick}!"
            for emoji in rps_emotes:
                await prompt.add_reaction(emoji)

            ''' USER INPUT '''

            def response_check(user_reaction, user):
                return user == ctx.message.author and user_reaction.emoji in rps_emotes

            try:
                user_input, user_name = await self.bot.wait_for('reaction_add', timeout=15.0, check=response_check)
            except asyncio.TimeoutError:
                await prompt.delete()
                await error_embed(ctx, "No choice was selected!")

            user_pick = ""
            if user_input.emoji == "🤘":
                user_pick = "Rock"
            elif user_input.emoji == "📃":
                user_pick = "Paper"
            elif user_input.emoji == "✂":
                user_pick = "Scissors"

            ''' GAME LOGIC '''
            winnings = 0
            if user_pick == bot_pick:
                embed.title = "It's a tie!"

            elif user_pick == "Rock":
                if bot_pick == "Scissors":
                    embed.title = "Rock crushes Scissors! =]"
                    winnings += 1
                if bot_pick == "Paper":
                    embed.title = "Paper covers Rock! = ("
                    winnings -= 1

            elif user_pick == "Paper":
                if bot_pick == "Rock":
                    embed.title = "Paper covers Rock! =>"
                    winnings += 1
                if bot_pick == "Scissors":
                    embed.title = "Scissors cut Paper! =|"
                    winnings -= 1

            elif user_pick == "Scissors":
                if bot_pick == "Paper":
                    embed.title = "Scissors cut Paper! >=}"
                    winnings += 1
                if bot_pick == "Rock":
                    embed.title = "Rock crush Scissors! ='("
                    winnings -= 1

            embed.set_footer(text=f"You won/lost: {winnings} BORB")
            await prompt.edit(embed=embed)

            if winnings > 0:
                change_money(ctx.author.id, winnings * wager)

        else:
            await error_embed(ctx, "You don't have that much to wager! 🤣")

    @rps.error
    async def rps_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await error_embed(ctx, "You didn't wager anything!\n"
                                   "Syntax: `.rps (wager amount)`")


def setup(bot):
    bot.add_cog(GamblingGames(bot))
