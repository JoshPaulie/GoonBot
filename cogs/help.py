from discord.ext import commands
import discord


class Help(commands.Cog, name="Help ℹ"):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def help(self, ctx):

        embed = discord.Embed(title="Available commands! 📜")

        all_bot_cogs = self.bot.cogs
        for cog_name, CogClass in all_bot_cogs.items():

            cog_cmds = CogClass.get_commands()
            cog_cmd_list = []

            for cmd in cog_cmds:
                cog_cmd_list.append(cmd.name)

            if len(cog_cmd_list) != 0:  # * ignore cogs that don't have any commands
                cmd_str = ", ".join(sorted(cog_cmd_list))
                embed.add_field(name=cog_name, value=cmd_str, inline=True)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
