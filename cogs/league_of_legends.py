import asyncio
import datetime

import discord
from discord.ext import commands
from riotwatcher import LolWatcher, ApiError

from helpers.LeagueOfLegends.league_helper import create_embed, win_loss_dict
from helpers.LeagueOfLegends.league_match_parser import MatchParser, latest
from modules.paulie_tools import calc_time, color_range, error_embed
from passwords_and_keys.RiotApiKey import riot_api_key

watcher = LolWatcher(riot_api_key())
region = 'na1'


class LeagueOfLegends(commands.Cog, name="League of Legends! 🎮"):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="matches", aliases=['matchhistory'])
    async def matches(self, ctx, summoner, match_count=3):
        """Pulls a summoner's last # games

        Syntax `.matches (summoner) (match count 1-15)`"""
        max_matches = 15
        if match_count <= max_matches:
            start_time = datetime.datetime.now()

            embed_match_list = discord.Embed(title=f"{summoner}'s last {match_count} games!")

            async with ctx.typing():
                try:
                    summoner_data = watcher.summoner.by_name(region, summoner)
                    account_id = summoner_data['accountId']
                    match_list = watcher.match.matchlist_by_account(region, account_id, begin_index=0,
                                                                    end_index=match_count)
                except ApiError as e:
                    if e.response.status_code == 429:
                        await ctx.send('Rate limited. Command terminated.')
                    elif e.response.status_code == 404:
                        await ctx.send("Summoner was not found.")
                    elif e.response.status_code == 504:
                        await error_embed(ctx, "Connect timeout. Try again.")

                for match in match_list['matches']:  # * Per match in match_list
                    match = MatchParser(summoner, match)
                    embed_match_list.add_field(name=f"{win_loss_dict[match.win]} [{match.queue_type}] {match.result}\n"
                                                    f"{match.champion}",
                                               value=f"⚔ **{match.kills}/{match.deaths}/{match.assists}** "
                                                     f"(**{match.dominance_factor}** DF)\n"
                                                     f"CS **{match.cs}** | Vision **{match.vision_score}**\n"
                                                     f"**{match.turret_kills}** Turret(s) | "
                                                     f"**{match.inhibitor_kills}** Inhib(s)\n"
                                                     f"*{match.human_game_creation}*\n"
                                                     f"〰️",
                                               inline=True)

            loading_time = datetime.datetime.now() - start_time
            embed_match_list.set_footer(text=f"Loading time: {loading_time.seconds}s\n")

            embed_match_list.colour = discord.Colour.from_rgb(color_range(), color_range(), color_range())
            match_list_messsage = await ctx.send(embed=embed_match_list)
            await match_list_messsage.add_reaction('🚮')
        else:
            await ctx.send(f"I'm sorry, but we can only look up {max_matches} matches at a time!")

    @commands.command(name="lastgame")
    async def lastgame(self, ctx, summoner):
        """Pulls the summoner's last game with detailed stats

        Syntax `.lastgame (summoner)`"""
        async with ctx.typing():
            try:
                summoner_data = watcher.summoner.by_name(region, summoner)
                account_id = summoner_data['accountId']
                match_list = watcher.match.matchlist_by_account(region, account_id, begin_index=0, end_index=1)
            except ApiError as e:
                if e.response.status_code == 429:
                    await error_embed(ctx, 'Rate limited. Command terminated.')
                elif e.response.status_code == 404:
                    await error_embed(ctx, "Summoner was not found.")
                elif e.response.status_code == 504:
                    await error_embed(ctx, "Connect timeout. Try again.")

        last_match = None
        for match in match_list['matches']:
            last_match = MatchParser(summoner, match)

        ''' Create Embed '''

        embed_last_game = discord.Embed(title=f'{summoner}',
                                        description=f"**{last_match.result}**\n"
                                                    f"Queue type **{last_match.queue_type}**\n"
                                                    f"Duration **{calc_time(last_match.game_duration, 'digit')}** "
                                                    f"({last_match.human_game_creation})")

        ''' Main Stats '''

        embed_last_game.add_field(name="KDA (K+A/D)",
                                  value=f"{last_match.kills}/{last_match.deaths}/{last_match.assists} "
                                        f"(**{last_match.kda_ratio}**)")
        embed_last_game.add_field(name="Dominance Factor", value=last_match.dominance_factor)
        embed_last_game.add_field(name="Kill participation", value=f"{last_match.kill_participation}%")
        if last_match.death_participation > 50:
            embed_last_game.add_field(name="Death participation", value=f"{last_match.death_participation}% 💀")
        embed_last_game.add_field(name="CS", value=last_match.cs)
        embed_last_game.add_field(name="Pinks Bought", value=last_match.pink_wards_bought)
        embed_last_game.add_field(name="Vision Score", value=last_match.vision_score)

        ''' Carry Stats '''

        if last_match.largest_killing_spree > 0:
            embed_last_game.add_field(name="Longest Spree", value=last_match.largest_killing_spree)

        embed_last_game.add_field(name="Damage Dealt", value=f"{last_match.total_damage_dealt: ,} "
                                                             f"(**{last_match.damage_participation}%**)")

        embed_last_game.add_field(name="Damage Taken", value=f"{last_match.total_damage_taken: ,}")

        embed_last_game.add_field(name="Objective Damage", value=f"{last_match.damage_dealt_to_objectives: ,} "
                                                                 f"(**{last_match.obj_damage_participation}%**)")

        if last_match.biggest_crit > 1000:
            embed_last_game.add_field(name="Biggest Crit ⚡", value=last_match.biggest_crit)

        embed_last_game.add_field(name="Longest Time Alive",
                                  value=f"{calc_time(last_match.longest_time_spent_living, 'digit')} "
                                        f"(**{last_match.percent_longest_living_duration}%**)")

        if last_match.total_time_cc_dealt > 200:
            embed_last_game.add_field(name="CC Dealt", value=f"{last_match.total_time_cc_dealt}s")

        if last_match.turret_kills > 0:
            embed_last_game.add_field(name="Turrets Destroyed", value=last_match.turret_kills)

        if last_match.inhibitor_kills > 0:
            embed_last_game.add_field(name="Inhibitors Destroyed", value=last_match.inhibitor_kills)

        ''' Game Highlights '''

        if last_match.first_tower_kill is True:
            embed_last_game.add_field(name="First tower!", value="🛡")
        if last_match.first_tower_assist is True:
            embed_last_game.add_field(name="First tower assist!", value="🛡")
        if last_match.first_blood_kill is True:
            embed_last_game.add_field(name="First blood!", value="🩸")

        ''' Multi Kills '''

        if last_match.double_kills > 0:
            embed_last_game.add_field(name="Double Kills! ✌", value=last_match.double_kills)
        if last_match.triple_kills > 0:
            embed_last_game.add_field(name="Triple Kills! 😏", value=last_match.triple_kills)
        if last_match.quadra_kills > 0:
            embed_last_game.add_field(name="Quadra Kills! 🔥", value=last_match.quadra_kills)
        if last_match.penta_kills > 0:
            embed_last_game.add_field(name="Penta Kills! 👑", value=last_match.penta_kills)

        ''' Embed Pretty '''

        if last_match.win is True:
            embed_last_game.colour = 0x3CB371
        else:
            embed_last_game.colour = 0xCD5C5C

        embed_last_game.set_thumbnail(url=f"http://ddragon.leagueoflegends.com/cdn/{latest}/img/champion/"
                                          f"{last_match.champion}.png")
        embed_last_game.set_footer(text="Dominance Factor is calculated as followed:\n"
                                        "Kills +2, Deaths -3, Assists +1")

        last_game_msg = await ctx.send(embed=embed_last_game)

        await last_game_msg.add_reaction('🚮')

    @commands.command(name="rank")
    async def rank(self, ctx, summoner):
        """Get's the rank of a league summoner!

        Syntax `.rank (summoner)`"""
        solo_stats = None
        flex_stats = None

        ''' Parsing of ranked data into solo or flex stats, if any '''

        async with ctx.typing():
            try:
                summoner_data = watcher.summoner.by_name(region, summoner)
                ranked_stats = watcher.league.by_summoner(region, summoner_data['id'])
            except ApiError as e:
                if e.response.status_code == 429:
                    await error_embed(ctx, 'Rate limited. Command terminated.')
                elif e.response.status_code == 404:
                    await error_embed(ctx, "Summoner was not found.")
                elif e.response.status_code == 504:
                    await error_embed(ctx, "Connect timeout. Try again.")

        for rank in ranked_stats:
            if 'RANKED_SOLO_5x5' == rank['queueType']:
                solo_stats = rank
            if 'RANKED_FLEX_SR' == rank['queueType']:
                flex_stats = rank

        if solo_stats is not None:
            await ctx.send(embed=create_embed(solo_stats))
        if flex_stats is not None:
            await ctx.send(embed=create_embed(flex_stats))

    @rank.error
    async def rank_error(self, ctx, error):
        message = ctx.message
        if isinstance(error, commands.MissingRequiredArgument):
            await error_embed(ctx, f"ℹ You need to add a summoner name!")


def setup(bot):
    bot.add_cog(LeagueOfLegends(bot))
