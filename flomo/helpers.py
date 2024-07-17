import os
import platform

from playsound import playsound

import flomo.config as config
import flomo.errors as errors


def get_path(file_name: str, in_data: bool = False):
    # TODO: Change data folder to documents folder (and the equivalent in other OSes).
    dir_path = os.path.dirname(os.path.realpath(__file__))

    sign = "\\" if platform.system().lower() == "windows" else "/"
    data_folder = f"{sign}data" if in_data else ""

    if in_data and not os.path.exists(dir_path + data_folder):
        os.makedirs(dir_path + data_folder)

    file = f"{data_folder}{sign}{file_name}"

    return os.path.join(dir_path + file)


def play_sound():
    try:
        path = get_path("beep.mp3")
        conf = config.Config()

        notification_priority: str = conf.get_config("notification_priority")

        if notification_priority.lower() == "off":
            return

        if not platform.system().lower() in ["windows", "darwin"]:
            priority = (
                "critical" if notification_priority.lower() == "high" else "normal"
            )
            os.system(
                f"notify-send 'Flomo' 'Time to start flowing!' -u {priority} && paplay "
                + path
            )
        else:
            playsound(path)
    except errors.NoConfigError:
        message_log("Config file not found.")


def message_log(message: str):
    path = get_path("message.log", in_data=True)

    with open(path, "a") as f:
        f.write(message + "\n")


def format_time(seconds: int) -> str:
    hours, remainder = divmod(seconds, 3600)
    mins, secs = divmod(remainder, 60)

    return f"{hours:02}:{mins:02}:{secs:02}"
