import datetime
import random
from pathlib import Path

import discord
from discord.ext import commands
from discord.ext.commands import BucketType

from modules.sql_helper import *

files_assets_path = Path("helpers")


def purchase_check(current_balance, cost_of_item):
    if current_balance < cost_of_item:
        return False
    else:
        return True


def mug_check():
    return random.randint(0, 5)


def get_voice_line(attacker, victim, result):
    voice_lines = None

    if result == 'winning':
        with open("helpers/mugging_voice_lines/winning_voice_lines.txt") as f:
            voice_lines = f.readlines()

    elif result == 'losing':
        with open("helpers/mugging_voice_lines/losing_voice_lines.txt") as f:
            voice_lines = f.readlines()

    elif result == 'losing_badly':
        with open("helpers/mugging_voice_lines/losing_badly_voice_lines.txt") as f:
            voice_lines = f.readlines()

    voice_line = random.choice(voice_lines)
    voice_line = voice_line.replace("[a]", attacker)
    voice_line = voice_line.replace("[v]", victim)
    return voice_line


class MuggingGame(commands.Cog, name="Mugging Game! 👊"):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # ! This isn't elegant, too bad!
    # TODO Revise this! How? That's for tomorrow josh!
    @commands.cooldown(1, random.randint(1800, 7200), type=BucketType.user)
    @commands.command(name='mug', aliases=['attack'], cooldown_after_parsing=True)
    async def mug(self, ctx, victim: discord.Member):
        """Attacks @user. <Results may vary>"""
        attacker = ctx.author
        victim_current_money = query(victim.id)[1]
        attacker_current_money = query(attacker.id)[1]

        # * The attack was successful.
        if mug_check() == 1:
            if purchase_check(victim_current_money, 1):
                change_money(ctx.author.id, 1)
                change_money(victim.id, -1)
                mugging_embed = discord.Embed(title="A mugging occurred!",
                                              description=get_voice_line(attacker.name, victim.name, "winning"))
                mugging_embed.add_field(name=f"{attacker.name}", value="+1", inline=True)
                mugging_embed.add_field(name=f"{victim.name}", value="-1", inline=True)
                await ctx.send(embed=mugging_embed)
            else:
                # * If you can't tell by the dialog, this is the only voice line if a
                # * mugging was successful but
                mugging_embed = discord.Embed(title="A mugging occurred!",
                                              description=f"{attacker.name} stole {victim.name}'s wallet, but it was "
                                                          f"void of BORB.")
                mugging_embed.colour = discord.Colour.green()
                await ctx.send(embed=mugging_embed)

        # * Went wrong, attacker lost money to the victim
        elif mug_check() == 2:
            if purchase_check(attacker_current_money, 1):
                change_money(ctx.author.id, -1)
                change_money(victim.id, 1)
                mugging_embed = discord.Embed(title="A mugging occurred?",
                                              description=get_voice_line(attacker.name, victim.name, "losing_badly"))
                mugging_embed.add_field(name=f"{attacker.name}", value="-1", inline=True)
                mugging_embed.add_field(name=f"{victim.name}", value="+1", inline=True)
                mugging_embed.colour = discord.Colour.greyple()
                await ctx.send(embed=mugging_embed)

        # * Attack was unsuccessful
        else:
            mugging_embed = discord.Embed(title="An attempted mugging occurred!",
                                          description=get_voice_line(attacker.name, victim.name, "losing"))
            mugging_embed.colour = discord.Colour.red()
            await ctx.send(embed=mugging_embed)

    @mug.error
    async def mugError(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            end_timestamp = datetime.datetime.now() + datetime.timedelta(0, error.retry_after)
            embed = discord.Embed(title=f"{ctx.author.name}, you're on cooldown!",
                                  description=f"{calc_time(error.retry_after)} remaining. "
                                              f"**{end_timestamp.strftime('%H:%M %p')}**",
                                  colour=discord.Colour.red())
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(MuggingGame(bot))
