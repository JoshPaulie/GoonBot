import discord
from discord import colour
from discord.ext import commands
from riotwatcher import LolWatcher, ApiError
import pprint
import random

from passwords_and_keys.RiotApiKey import riot_api_key

watcher = LolWatcher(riot_api_key())
region = 'na1'


def calc_wr(wins, losses):
    reaction = None
    wr = round((wins / (losses + wins) * 100))
    if wr >= 55:
        reaction = '👑 WOW!'
    elif wr == 53 or wr == 54:
        reaction = '🤩'
    elif wr == 52 or wr == 53:
        reaction = '😎'
    elif wr == 50 or wr == 51:
        reaction = '😄'
    elif wr == 49:
        reaction = '🙃'
    elif wr == 48:
        reaction = '😅'
    elif wr <= 47:
        reaction = '😶'

    return f"{wr}% {reaction}"


def embed_color_by_tier(rank):
    if rank == 'IRON':
        return 0x565050
    elif rank == 'BRONZE':
        return 0xA0644D
    elif rank == 'SILVER':
        return 0x9CA5AA
    elif rank == 'GOLD':
        return 0xF2C066
    elif rank == 'PLATINUM':
        return 0x53C999
    elif rank == 'DIAMOND':
        return 0x9DB0DB
    elif rank == 'MASTER':
        return 0xD792C9
    elif rank == 'GRANDMASTER':
        return 0xF96065
    elif rank == 'CHALLENGER':
        return 0xFFF5D3


def create_embed(rank_stats):
    # * PARSED DATA
    wins = rank_stats['wins']
    losses = rank_stats['losses']
    win_rate = calc_wr(wins, losses)
    tier = rank_stats['tier']  # * BRONZE, GOLD, ETC
    rank = rank_stats['rank']  # * I, II, ETC
    lp = rank_stats['leaguePoints']
    streak = rank_stats['hotStreak']
    queue_type = rank_stats['queueType']
    p_summoner_name = rank_stats['summonerName']

    # * EMBED
    current_queue_type = None
    symbol = None
    if queue_type == "RANKED_SOLO_5x5":
        current_queue_type = "Solo/Duo"
        symbol = '🏆'
    elif queue_type == "RANKED_FLEX_SR":
        current_queue_type = "Flex/Team"
        symbol = '💪'

    embed = discord.Embed(title=f"{p_summoner_name}'s {current_queue_type} Queue Stats! {symbol}")
    embed.add_field(name="Standing!",
                    value=f"{tier} {rank} ({lp} LP)",
                    inline=True)
    embed.add_field(name="Performance!",
                    value=f"{wins}/{losses} | {win_rate}",
                    inline=True)

    embed.colour = embed_color_by_tier(tier)

    if streak is True:
        embed.description = f"🔥 {p_summoner_name} is on a hot streak!!"

    return embed


class LoLRank(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="rank")
    async def rank(self, ctx, summoner):
        """Get's the rank of a league summoner!"""
        solo_stats = None
        flex_stats = None

        ''' Parsing of ranked data into solo or flex stats, if any '''
        async with ctx.typing():
            try:
                summoner_data = watcher.summoner.by_name(region, summoner)
                ranked_stats = watcher.league.by_summoner(region, summoner_data['id'])
            except ApiError as e:
                await ctx.send(e)

        for rank in ranked_stats:
            if 'RANKED_SOLO_5x5' == rank['queueType']:
                solo_stats = rank
            if 'RANKED_FLEX_SR' == rank['queueType']:
                flex_stats = rank

        if solo_stats is not None:
            await ctx.send(embed=create_embed(solo_stats))
        if flex_stats is not None:
            await ctx.send(embed=create_embed(flex_stats))

        debug_mode = False
        if debug_mode:
            print('SOLO STATS')
            pprint.pprint(solo_stats)
            print(type(solo_stats))
            print()
            print('FLEX STATS')
            pprint.pprint(flex_stats)
            print(type(flex_stats))
            print('\n-------\n')

    @rank.error
    async def rank_error(self, ctx, error):
        goon_names = ['bexli', 'boxrog', 'roninalex', 'poydok', 'mltsimpleton']
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Please enter a summoner name!\nExample: `.rank {random.choice(goon_names)}`")


def setup(bot):
    bot.add_cog(LoLRank(bot))
