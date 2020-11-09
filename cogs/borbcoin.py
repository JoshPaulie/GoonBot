import random
from pathlib import Path

import discord
from discord.ext import commands

from modules.sql_helper import query, qall, change_money

files_assets_path = Path("files_assets")


def purchase_check(current_balance, cost_of_item):
    if current_balance < cost_of_item:
        return False
    else:
        return True


class BorbCoin(commands.Cog):

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
                self.borb_chance = random.randint(200, 800)
                await message.add_reaction('<:borb:452006705035739136>')
                change_money(message.author.id, 1)
                embed = discord.Embed(title=f"{message.author.name} mined 1 BORB!",
                                      description=f"New BORB value: **1:{self.borb_chance}**")
                await self.bot_channel.send(embed=embed)

    @commands.command(name='balance', aliases=['wallet'])
    async def balance(self, ctx, user: discord.Member = None):
        '''Checks balance of yourself, or @user'''
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
            await ctx.send("This feature is currently broken. 🙁")

    # Sends borb from one wallet, to anothers
    @commands.command(name='borb', aliases=['gift', 'give', 'send'])
    async def borb(self, ctx, user: discord.Member = None, donate_amount: int = 1, *, note=None):
        '''Sends x amount of BORB to recipient'''
        message = ctx.message

        if user is not None:
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
                await message.author.send("I'm sorry, you don't have any BORB to gift. 😶")
        else:
            await ctx.send("You need to pick a recipient! 😎")

    # @mine.error
    # async def mineError(self, ctx, error):
    #     if isinstance(error, commands.CommandOnCooldown):
    #         await ctx.send(f"You are tired and recently went mining.. Please wait **{calc_time(error.retry_after)}**")

    @commands.command(name='faq', aliases=['borbcoin'])
    async def bscFAQ(self, ctx):
        embed = discord.Embed(title="Borb Coin FAQ! <:borb:452006705035739136>",
                              description="Borb Coin (BORB) is the latest in cutting edge cryptocurrency.",
                              inline=False)
        embed.add_field(name="How do I earn BORB?",
                        value="A lesser known feature of Goonbot is BorbBot. He determines who has earned them.",
                        inline=True)
        embed.add_field(name="What are the odds of me getting a BORB?",
                        value=f"1:{str(self.borb_chance)}\nA new value is determined after every new BORB is issued.",
                        inline=True)
        embed.add_field(name="How do I gift someone one of my BORB?",
                        value="`.borb @user [quantity] [note]`\nThe default amount is 1. An optional note can be attached.",
                        inline=True)
        embed.add_field(name="How do I check my balance?", value="`.balance` or `.wallet`\nEveryone starts with "
                                                                 "5.\nYou can also `.balance @user`",
                        inline=True)
        embed.add_field(name="Does adding a BORB reaction do anything?",
                        value="**NO**.", inline=True)
        embed.add_field(name="What is mugging?",
                        value="You pick a fight with a discord member\n20% You are successful\n20% You lose, badly\n60% The attack fails",
                        inline=True)
        embed.set_footer(text="*BORB Coin Council Members: Jaowsh, Poydok, Ectoplax")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(BorbCoin(bot))
