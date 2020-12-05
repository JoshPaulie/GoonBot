import discord

wr_reaction = {
    100: '👑 PERFECT!!',
    99: '👑 OH HOLY SHIT?!',
    98: '👑 A+++!!',
    97: '🐄 HOLY COW!!',
    96: '👑 GODGAMER!!',
    95: '👑 BIGGLY-BOY!!',
    94: '🧮 Scripter!!',
    93: '👑 BLESSED.',
    92: '👑 SUPER!!',
    91: '👑 WOWZA!!',
    90: '👑 BOYOYOYOYING!',
    89: '😈 TOP TIER!',
    88: '‼ WOW!',
    87: '🌟 HOLY!',
    86: '⭐ JEEZ WHIZZ!',
    85: '✨ YAOOW!',
    84: '🧠',
    83: '🧠',
    82: '🤓',
    81: '🤓',
    80: '😉',
    79: '😉',
    78: '🤑',
    77: '🤑',
    76: '😏',
    75: '😏',
    74: '😛',
    73: '😛',
    72: '😝',
    71: '😝',
    70: '😜',
    69: '♋️',
    68: '😜',
    67: '👅',
    66: '👅',
    65: '🦾',
    64: '🦾',
    63: '🤤',
    62: '🤤',
    61: '🤗',
    60: '🤗',
    59: '😸',
    58: '🤩',
    57: '🤩',
    56: '😎',
    55: '😎',
    54: '😀',
    53: '😀',
    52: '🙂',
    51: '🙂',
    50: '😗',
    49: '😗',
    48: '😅',
    47: '😅',
    46: '😐',
    45: '😐',
    44: '😑',
    43: '😑',
    42: '🤐',
    41: '🤐',
    40: '💀',
    39: '💀',
    38: '😹',
    37: '😹',
    36: '😂',
    35: '😂',
    34: '🤣',
    33: '🤣',
    32: '😔',
    31: '😔',
    30: '😟',
    29: '😟',
    28: '😣',
    27: '😣',
    26: '😖',
    25: '😖',
    24: '😞',
    23: '😞',
    22: '🙁',
    21: '🙁',
    20: '😶',
    19: '😶',
    18: '😶',
    17: '😶',
    16: '😶',
    15: '😶',
    14: '😶',
    13: '😶',
    12: '😶',
    11: '😶',
    10: '😶',
    9: '😶',
    8: '😶',
    7: '😶',
    6: '😶',
    5: '😶',
    4: '😶',
    3: '😶',
    2: '😶',
    1: '😶'
}

win_loss_dict = {
    True: "🏆",
    False: "🥈"
}


def calc_wr(wins, losses):
    wr = round((wins / (losses + wins) * 100))
    return f"{wr}% {wr_reaction[wr]}"


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

    embed.colour = embed_tier[tier]

    if streak is True:
        embed.description = f"🔥 {p_summoner_name} is on a hot streak!!"

    return embed


embed_tier = {
    'IRON': 0x565050,
    'BRONZE': 0xA0644D,
    'SILVER': 0x9CA5AA,
    'GOLD': 0xF2C066,
    'DIAMOND': 0x9DB0DB,
    'PLATINUM': 0xA0644D,
    'MASTER': 0xD792C9,
    'GRANDMASTER': 0xF96065,
    'CHALLENGER': 0xFFF5D3,
}