import datetime
from datetime import timedelta
import random


def calc_time(in_seconds: int, time_format: str = "text"):
    td = timedelta(seconds=int(in_seconds))
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours == 0 and minutes > 0:
        if time_format == "text":
            return f"{minutes} minute(s) and {seconds} second(s)"
        elif time_format == "digit":
            return f"{minutes}:{seconds}"

    if hours == 0 and minutes == 0:
        if time_format == "text":
            return f"{seconds} second(s)"
        elif time_format == "digit":
            return f"00:{seconds}"

    else:
        if time_format == "text":
            return f"{hours} hour(s) {minutes} minute(s) and {seconds} second(s)"
        elif time_format == "digit":
            return f"{hours}:{minutes}:{seconds}:"


def current_time():
    now = datetime.datetime.now()
    return f"{now.strftime('%b. %d %I:%M %p')}"


def random_game_name():
    with open('helpers/goonbots_brain/bot_game_list.txt') as f:
        games = f.readlines()
        game_name = random.choice(games)
        return game_name
