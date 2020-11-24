from pathlib import Path

import discord
from discord.ext import commands

files_assets_path = Path("helpers")


class MinecraftInfo(commands.Cog, name="Minecraft Info! ⛏"):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name='minecraft', aliases=['mc', 'ip', 'server'])
    async def minecraft(self, ctx):
        """Minecraft Server Information"""
        message = ctx.message
        embed = discord.Embed(title="Gooner Gulf (On Apex) - Minecraft Server",
                              description='😵 "is this the same map?" Yes!', color=0x2fc153)
        embed.add_field(name="🌐 IP Address", value="`gooner.apexmc.co`", inline=True)
        embed.add_field(name="💪 Alt. IP Address", value="`45.35.213.228:25627`", inline=True)
        embed.add_field(name="🗺 Map!", value="http://45.35.213.228:4355/", inline=True)
        embed.add_field(name="⚡ RAM (Doe-deditated)", value="`4gb`", inline=True)
        embed.add_field(name="🕵️ Whitelist Enabled", value="Ping Josh or Vynle to be added.", inline=True)
        embed.add_field(name="🌳 Seed", value="1500915975625339518", inline=True)
        embed.add_field(name="👑 Donor(s):", value="- Alex ($10)\n- Justin ($10)\n- Daniel ($10)\n- Chris ($10)\n- Lex ($10)", inline=True)
        await ctx.send(embed=embed)

    @commands.command(name='map')
    async def map(self, ctx):
        """Replies with link to MC map"""
        embed = discord.Embed(title='🗺 A Live Map of Gooner Gulf!', description='http://45.35.213.228:4355/')
        await ctx.send(embed=embed)

    @commands.command(name="mchelp", aliases=['minecrafthelp', 'helpmc'])
    async def minecrafthelp(self, ctx):
        """Links for Minecraft help"""
        embed = discord.Embed(title="Quick Minecraft Help",
                              description="Plan B - Ping @jaowsh")
        embed.add_field(name="It says my version is out-of-date!",
                        value="https://bexli.xyz/how-to-set-minecraft-to-latest-version")
        embed.add_field(name="The server doesn't work!",
                        value="- `.mc` will let you if the official* server is online\n"
                              "- Double check the IP you have entered\n"
                              "- Try the alt IP\n"
                              "- You might be trying to connect to the old IP address")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(MinecraftInfo(bot))
