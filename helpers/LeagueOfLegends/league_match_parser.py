import arrow
from riotwatcher import LolWatcher

from passwords_and_keys.RiotApiKey import riot_api_key

watcher = LolWatcher(riot_api_key())
region = 'na1'
latest = watcher.data_dragon.versions_for_region(region)['n']['champion']

q_types = {
    400: "Normal",
    420: "Solo/Duo",
    430: "Blind Pick",
    440: "Flex Queue",
    450: "ARAM"
}


def get_champs():
    return watcher.data_dragon.champions(latest, False, 'en_US')


def champ_by_id(id_champ: int):
    data = get_champs()
    for champ_name, champ_data in data['data'].items():
        if int(champ_data['key']) == id_champ:
            return champ_name


class MatchParser:
    def __init__(self, summoner, match):
        self.summoner = summoner
        self.match = match

        summoner_data = watcher.summoner.by_name(region, summoner)
        account_id = summoner_data['accountId']
        match_id = match['gameId']
        match_data = watcher.match.by_id(region, match_id)

        participant_id = None

        for participant in match_data['participantIdentities']:
            if participant['player']['accountId'] == account_id:
                participant_id = participant['participantId']

        for participant in match_data['participants']:  # * Checks all participants ⤵
            if participant_id == participant['participantId']:  # * If participant is who we want
                self.team_id = participant['teamId']
                self.champion_id = participant['championId']
                self.champion = champ_by_id(self.champion_id)
                self.queue_type = q_types[match_data['queueId']]
                self.game_duration = match_data['gameDuration']
                self.game_creation = match_data['gameCreation']
                self.human_game_creation = arrow.get(self.game_creation).humanize()

                self.win = participant['stats']['win']
                self.kills = participant['stats']['kills']
                self.deaths = participant['stats']['deaths']
                self.assists = participant['stats']['assists']
                self.dominance_factor = (self.kills * 2) + (self.deaths * -3) + (self.assists * 1)
                self.longest_time_spent_living = participant['stats']['longestTimeSpentLiving']
                self.percent_longest_living_duration = round(
                    (self.longest_time_spent_living / self.game_duration) * 100, 2)

                self.kda_ratio = None
                if self.deaths != 0:
                    self.kda_ratio = round((self.kills + self.assists) / self.deaths, 2)
                else:
                    self.kda_ratio = "PERF"

                self.lane = participant['timeline']['lane']
                self.first_blood_kill = participant['stats']['firstBloodKill']
                self.first_tower_kill = participant['stats']['firstTowerKill']
                self.first_tower_assist = participant['stats']['firstTowerAssist']
                self.total_minions_killed = participant['stats']['totalMinionsKilled']
                self.neutral_minions_killed = participant['stats']['neutralMinionsKilled']
                self.neutral_minions_killed_team_jungle = participant['stats']['neutralMinionsKilledTeamJungle']
                self.neutral_minions_killed_enemy_jungle = participant['stats']['neutralMinionsKilledEnemyJungle']
                self.cs = self.total_minions_killed + self.neutral_minions_killed

                self.largest_killing_spree = participant['stats']['largestKillingSpree']
                self.double_kills = participant['stats']['doubleKills']
                self.triple_kills = participant['stats']['tripleKills']
                self.quadra_kills = participant['stats']['quadraKills']
                self.penta_kills = participant['stats']['pentaKills']

                self.total_damage_dealt = participant['stats']['totalDamageDealt']
                self.total_damage_taken = participant['stats']['totalDamageTaken']
                self.damage_dealt_to_objectives = participant['stats']['damageDealtToObjectives']
                self.vision_score = participant['stats']['visionScore']
                self.pink_wards_bought = participant['stats']['visionWardsBoughtInGame']
                self.turret_kills = participant['stats']['turretKills']
                self.inhibitor_kills = participant['stats']['inhibitorKills']
                self.total_healing = participant['stats']['totalHeal']
                self.total_time_cc_dealt = participant['stats']['totalTimeCrowdControlDealt']
                self.biggest_crit = participant['stats']['largestCriticalStrike']

                self.result = None
                if self.win is True:
                    self.result = "Victory!"
                else:
                    self.result = "Defeat."

        self.team_kills = 0
        self.team_deaths = 0
        self.team_assists = 0
        self.team_damage_dealt = 0
        self.team_obj_damage = 0
        for participant in match_data['participants']:
            if self.team_id == participant['teamId']:
                self.team_kills += participant['stats']['kills']
                self.team_deaths += participant['stats']['deaths']
                self.team_assists += participant['stats']['assists']
                self.team_damage_dealt += participant['stats']['totalDamageDealt']
                self.team_obj_damage += participant['stats']['damageDealtToObjectives']

        self.kill_participation = round(((self.kills + self.assists) / self.team_kills) * 100)
        self.death_participation = round((self.deaths / self.team_deaths) * 100)
        self.damage_participation = round((self.total_damage_dealt / self.team_damage_dealt) * 100)
        self.obj_damage_participation = round((self.damage_dealt_to_objectives / self.team_obj_damage) * 100)
