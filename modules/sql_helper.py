import sqlite3  # In order to connect to a sqlite database we will need to import this library which will allow us to
from datetime import timedelta

# communicate with the database
connection = sqlite3.connect("goonbase.db")
cursor = connection.cursor()


def initialize():
    try:
        cursor.execute('''CREATE TABLE Economy(
        id BIGINT PRIMARY KEY,
        borbcoin integer
        );''')
    except sqlite3.OperationalError as e:
        pass

        # ID, MONEY -> BASED COIN


def query(user_id: int):  # Query makes sure users are in db & get values.
    cursor.execute("SELECT * FROM Economy WHERE id=?", (user_id,))
    data = cursor.fetchone()
    starting_amount = 5
    if data is None:  # Creates user if not already in table
        cursor.execute('INSERT INTO Economy(id, borbcoin) VALUES (?,?)', (user_id, starting_amount,))
        data = (user_id, starting_amount)  # Determines how much we start
        connection.commit()
    # Query needs to be ran for every command
    return data

def qall():
    cursor.execute("SELECT * FROM Economy ORDER BY borbcoin DESC")
    alldata = cursor.fetchall()
    return alldata


def change_money(user_id, change_in_money: int):
    data = query(user_id)  # Makes sure user is in table
    current_money = data[1]  # Looks in middle col, the money/wallet balance
    new_money = current_money + change_in_money
    if new_money < 0:
        new_money = 0
    cursor.execute("UPDATE Economy SET borbcoin=? WHERE id=?", (new_money, user_id,))
    connection.commit()


def calc_time(in_seconds: int):
    td = timedelta(seconds=int(in_seconds))
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours == 0 and minutes > 0:
        return f"{minutes} minute(s) and {seconds} second(s)"
    if hours == 0 and minutes == 0:
        return f"Only {seconds} more second(s)"
    else:
        return f"{hours} hour(s) {minutes} minute(s) and {seconds} second(s)"