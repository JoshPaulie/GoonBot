from discord.ext import commands
import discord


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def help(self, ctx):
        """"""
        embed_help = discord.Embed(title="Help")

        embed_help.add_field(name="Art 🎨",
                             value="bringe, fword, pizza, clown, puke, ygg, frog, soy, joker",
                             inline=False)

        embed_help.add_field(name="Affirmations ❤",
                             value="cily, jyb",
                             inline=False)

        embed_help.add_field(name="BORB Coin 💰",
                             value="balance, ~~bank~~, borb, faq, mug, scratcher",
                             inline=False)

        embed_help.add_field(name="General ⚙",
                             value="coinflip, pfp, poll, virus",
                             inline=False)

        embed_help.add_field(name="Birthdays & Holidays 🎂",
                             value="bday, holiday (both do the same thing)",
                             inline=False)

        embed_help.add_field(name="League Stats 🏆",
                             value="rank, lastgame, matches",
                             inline=False)

        embed_help.add_field(name="Links 🌐",
                             value="paypig, github, jerma",
                             inline=False)

        embed_help.add_field(name="Category tags ℹ",
                             value="art, love, gen, bday, league, links")

        embed_help.set_footer(text="Commands can be expanded by category tag.\n"
                                   "Try .help (tag) for more info on a command")

        if ctx.invoked_subcommand is None:
            await ctx.send(embed=embed_help)

    @commands.command(name="help")
    async def help(self, ctx):
        """"""
        message = ctx.message

    @help.command()
    async def art(self, ctx):
        art_dict = {
            "bringe": "Better cringe, duh.",
            "fword": "Devil child",
            "pizza": "Xtra sauce",
            "clown": "Laughs",
            "puke": "🤮",
            "ygg": "You good girl?",
            "frog": "feeeeeet",
            "soy": "beta milk",
            "joker": "joka, baby!"
        }
        embed = discord.Embed(title="Art Help",
                              description="Various pieces of goon-curated art")
        for k, v in art_dict.items():
            embed.add_field(name=k, value=v)
        await ctx.send(embed=embed)

    @help.command()
    async def love(self, ctx):
        love_dict = {
            "cily": "Conrad, I love you",
            "jyb": "Justin, I love you"
        }

        embed = discord.Embed(title="Love Help",
                              description="Used to send affirmations to fellow Gooners 🤗")
        for k, v in love_dict.items():
            embed.add_field(name=k, value=v)
        await ctx.send(embed=embed)

    @help.command()
    async def Borb(self, ctx):
        borb_dict = {
            "borb": "Sends one BORB to ",
            "jyb": "Justin, I love you"
        }

        embed = discord.Embed(title="Love Help",
                              description="Used to send affirmations to fellow Gooners 🤗")
        for k, v in borb_dict.items():
            embed.add_field(name=k, value=v)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
