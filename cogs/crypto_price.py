import pprint

import discord
from discord.ext import commands
from nomics import Nomics

from modules.paulie_tools import color_range
from helpers.crypto_prices.coin_data_parser import CryptoParser

nomics = Nomics("655a218a1cfb289001a572260b8a4708")


class CryptoPrices(commands.Cog, name="Crypto Prices 📈"):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="crypto", aliases=['price', 'prices', 'value'])
    async def crypto(self, ctx, *symb):
        """Shows current price and 7 day change of coin, or coins.

        Syntax: `.crypto (symbol(s): optional)`
        Example: `.crypto btc link`"""
        default_symbols = ["BTC", "LINK", "ETC", "XRP", "LTC", "BCH"]
        default_symbols = sorted(default_symbols)

        if len(symb) != 0:
            lookup_ids = ", ".join(symb).upper()
        else:
            lookup_ids = ", ".join(default_symbols)

        async with ctx.typing():
            coin_data = nomics.Currencies.get_currencies(ids=lookup_ids)

        embed = discord.Embed(title="Crypto Prices",
                              description="Prices pulled from Nomics! 🤖\n"
                                          "*Shows current price & 7 day change*")
        for coin in coin_data:
            coin = CryptoParser(coin)
            embed.add_field(name=f"{coin.name} ({coin.symbol})",
                            value=f"{coin.str_price} "
                                  f"{coin.str_seven_change}")

        embed.colour = discord.Color.from_rgb(color_range(), color_range(), color_range())
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CryptoPrices(bot))
