from pathlib import Path

import colored
import discord
from colored import stylize
from discord.ext import commands, tasks

from modules.paulie_tools import current_time, random_game_name
from modules.sql_helper import initialize
from passwords_and_keys.discord_bot_token import discord_bot_token

intents = discord.Intents(messages=True, guilds=True, reactions=True)
bot = commands.Bot(command_prefix='.', case_insensitive=True, intents=intents, help_command=None)
files_assets_path = Path("helpers")


def collect_cogs():
    files = Path("cogs").rglob("*.py")
    for file in files:
        if "__init__" not in file.name:
            yield file.as_posix()[:-3].replace("/", ".")


def load_cogs():
    good_loads = 0
    for cog in collect_cogs():
        try:
            bot.load_extension(cog)
            good_loads += 1
        except Exception as e:
            print(f"Failed to load cog {cog}\n{e}")
    print(f"{stylize(current_time(), colored.fg(110))} {good_loads} Cogs loaded! Logging in...")


@bot.event
async def on_ready():
    print(f'{stylize(current_time(), colored.fg(120))} Successfully have logged in as {bot.user}')
    initialize()
    await bot.change_presence(activity=discord.Game(name=random_game_name()))


@tasks.loop(minutes=60)
async def game_changer(self):
    """Every hour, change the game to new addition on game list"""
    await bot.change_presence(activity=discord.Game(name=random_game_name()))


# Command processor
@bot.event
async def on_message(message):
    await bot.process_commands(message)


@bot.command(name='game', aliases=['playing', 'addgame'])
async def playing_game(ctx, *, game):
    """Adds game being library, to be played by bot"""
    await bot.change_presence(activity=discord.Game(name=game))
    with open(files_assets_path / 'bot_game_list.txt', mode='w') as file:
        file.write(f'{game}')
    await ctx.send(f"{game} was added to Goonbot's Steam Library!")


collect_cogs()
load_cogs()
bot.run(discord_bot_token())
