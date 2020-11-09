import datetime
from datetime import timedelta
import random


def calc_time(in_seconds: int):
    td = timedelta(seconds=int(in_seconds))
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours == 0 and minutes > 0:
        return f"{minutes} minute(s) and {seconds} second(s)"
    if hours == 0 and minutes == 0:
        return f"{seconds} second(s)"
    else:
        return f"{hours} hour(s) {minutes} minute(s) and {seconds} second(s)"


def current_time():
    now = datetime.datetime.now()
    return f"[{now.strftime('%b. %d %I:%M %p')}]"


def random_game_name():
    with open('files_assets/bot_game_list.txt') as f:
        games = f.readlines()
        game_name = random.choice(games)
        return game_name
