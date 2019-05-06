from apps.scoreboard.utils import create_key


def initialize_keys():
    create_key("installed", False)
    create_key("ctf_name", None)
    create_key("start_time", None)
    create_key("end_time", None)
    create_key("logo", None)
    create_key("theme", "core")
