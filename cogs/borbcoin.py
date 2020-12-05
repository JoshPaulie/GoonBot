import random
from pathlib import Path

import discord
from discord.ext import commands

from modules.paulie_tools import error_embed
from modules.sql_helper import query, qall, change_money

files_assets_path = Path("helpers")


def purchase_check(current_balance, cost_of_item):
    if current_balance < cost_of_item:
        return False
    else:
        return True


class BorbCoin(commands.Cog, name="Borbcoin! 💰"):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot_channel = self.bot.get_channel(477308735732187136)
        self.borb_chance = random.randint(200, 800)

        print(f'BORB chance is 1:{self.borb_chance}')

    @commands.Cog.listener()  # Hands out BORBS, "borb bot"
    async def on_message(self, message):
        ranNum = random.randint(0, self.borb_chance)
        if 'b.' not in message.content:  # ignore bongo commands
            if ranNum == 1:
                self.borb_chance = random.randint(200, 1000)
                await message.add_reaction('<:borb:452006705035739136>')
                change_money(message.author.id, 1)
                embed = discord.Embed(title=f"{message.author.name} mined 1 BORB!",
                                      description=f"New BORB value: **1:{self.borb_chance}**")
                await self.bot_channel.send(embed=embed)

    @commands.command(name='balance', aliases=['wallet'])
    async def balance(self, ctx, user: discord.Member = None):
        """Checks balance of yourself, or @user

        Syntax: `.borb @user`"""
        message = ctx.message
        borb_amount = None
        if user is None:
            data = query(ctx.author.id)
            user = message.author
            borb_amount = data[1]
        else:
            data = query(user.id)
            borb_amount = data[1]
        embed = discord.Embed(title=f"{user.display_name}'s Bank Account")
        embed.add_field(name="Balance", value=f"{borb_amount}")
        embed.set_footer(text=f"BORB Chance (Per Message): {self.borb_chance}")
        await ctx.send(embed=embed)

    @commands.command(name='bank')
    async def bank(self, ctx):
        """Leader-board style balances of everyone's wallet"""
        message = ctx.message
        try:
            balances = qall()
            scoreboard = discord.Embed(title="Bank Balances! 🤑",
                                       description="Who's got the most BORB? <:borb:452006705035739136>")
            for goon in balances:
                goonname = self.bot.get_user(goon[0]).name
                scoreboard.add_field(name=goonname, value=goon[1], inline=True)
            scoreboard.set_footer(text=f'Current value: 1:{self.borb_chance}')
            await ctx.send(embed=scoreboard)
        except:
            await error_embed(ctx, "This feature is currently broken. 🙁\n"
                                   "I don't know why. It keeps me up at night.")

    @commands.command(name='borb', aliases=['gift', 'give', 'send'])
    async def borb(self, ctx, user: discord.Member, donate_amount: int = 1, *, note=None):
        """Sends x amount of BORB to recipient

        Syntax: `.borb @user (Number Amount) (Optional Note)`"""
        message = ctx.message
        data = query(ctx.author.id)
        current_money = data[1]
        if purchase_check(current_money, donate_amount):
            change_money(ctx.author.id, -donate_amount)
            change_money(user.id, donate_amount)
            embed = discord.Embed(title=f"{donate_amount} BORB Transferred", description=f"{note}")
            embed.add_field(name="Recipient", value=user.name, inline=True)
            embed.add_field(name="Sender", value=ctx.author.name, inline=True)
            await ctx.send(embed=embed)
        else:
            await error_embed(ctx, "I'm sorry, but you don't that much BORB to gift. 😶")

    @borb.error
    async def borb_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await error_embed(ctx, "You need to pick a recipient! 🕶")

        if isinstance(error, commands.BadArgument):
            await error_embed(ctx, 'Command syntax: `.borb @user [donate_amount: number] [note: optional]`')


def setup(bot):
    bot.add_cog(BorbCoin(bot))
