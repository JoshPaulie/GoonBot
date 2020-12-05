import discord
from discord.ext import commands
from discord.utils import get

from modules.paulie_tools import color_range, error_embed


def cmd_lookup_embed(curious_cmd):
    embed = discord.Embed(title=f"{curious_cmd.name} (Extended Help)", description=f"{curious_cmd.help}")

    if len(curious_cmd.aliases) != 0:
        embed.add_field(name="Aliases", value=", ".join(curious_cmd.aliases))
    else:
        embed.add_field(name="Aliases", value="*None*")

    embed.colour = discord.Colour.from_rgb(color_range(), color_range(), color_range())
    return embed


class Help(commands.Cog, name="Help ℹ"):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    def available_commands_embed(self):
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

        embed.colour = discord.Colour.from_rgb(color_range(), color_range(), color_range())
        embed.set_footer(text="You can expand any command with .help <command> 🙂")

        return embed

    @commands.command(name="help")
    async def help(self, ctx, cmd=None):
        # ! I think this is a redundant mess, too bad! ⤵
        help_message = None
        if cmd is None:
            help_message = await ctx.send(embed=self.available_commands_embed())
        else:
            if curious_cmd := get(self.bot.commands, name=cmd):
                help_message = await ctx.send(embed=cmd_lookup_embed(curious_cmd))
            else:
                await error_embed(ctx, "**Unknown command** Type `.help` for a full list of command names\n\n"
                                       "**You can't look up commands by alias**")
        await help_message.add_reaction('🚮')


def setup(bot):
    bot.add_cog(Help(bot))
