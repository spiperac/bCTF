from config import set_key, get_key


def set_scoreboard_show(number_users):
    set_key("scoreboard_users", number_users)


def set_scoreboard_show():
    scoreboard_users = get_key("scoreboard_users")
    if scoreboard_users:
        return scoreboard_users
    else:
        return 0