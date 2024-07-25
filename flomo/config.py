import json
import os

import flomo.errors as errors
import flomo.helpers as helpers

# BUG: Sometimes, the config when changed ends up with a extra '}' at the end

default_session_data = {
    "tag": "Work",
    "name": "Working",
}

tag_colors = {"Work": "red", "Study": "blue", "Exercise": "green"}


DEFAULT_SESSION_DATA = "default_session_data"
NOTIFICATION_PRIORITY = "notification_priority"
TAG_COLORS = "tag_colors"


class Config:
    def __init__(
        self, initializing: bool = False, get_default_session_data: bool = False
    ):
        self.path = helpers.get_path("config.json", in_data=True)
        self.do_check = not initializing and not get_default_session_data

        if self.do_check and self._get_missing_keys() != []:
            raise errors.NoConfigError()

    def _config_file_exists(self):
        missing_keys = self._get_missing_keys()
        return os.path.exists(self.path), missing_keys

    def _get_missing_keys(self):
        if not os.path.exists(self.path):
            return [DEFAULT_SESSION_DATA, NOTIFICATION_PRIORITY, TAG_COLORS]

        with open(self.path, "r") as f:
            data = json.load(f)
            missing_keys = []

            if (
                DEFAULT_SESSION_DATA not in data
                or data[DEFAULT_SESSION_DATA].keys() != default_session_data.keys()
            ):
                missing_keys.append(DEFAULT_SESSION_DATA)

            if NOTIFICATION_PRIORITY not in data or data[
                NOTIFICATION_PRIORITY
            ].lower() not in ["off", "normal", "high"]:
                missing_keys.append(NOTIFICATION_PRIORITY)

            if TAG_COLORS not in data:
                missing_keys.append(TAG_COLORS)

            return missing_keys

    def create_config(self):
        file_exists, missing_keys = self._config_file_exists()
        if file_exists and missing_keys == []:
            return

        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump({}, f)

        with open(self.path, "r+") as f:
            data = json.load(f)
            for missing_key in missing_keys:
                if missing_key == DEFAULT_SESSION_DATA:
                    data[missing_key] = default_session_data
                if missing_key == NOTIFICATION_PRIORITY:
                    data[missing_key] = "normal"
                if missing_key == TAG_COLORS:
                    data[missing_key] = tag_colors

            f.seek(0)
            json.dump(data, f, indent=4)

    def get_config(self, key: str):
        if key == DEFAULT_SESSION_DATA and not self._config_file_exists()[0]:
            return default_session_data

        try:
            with open(self.path, "r") as f:
                data = json.load(f)
                return data[key]
        except KeyError:
            raise errors.InvalidConfigKeyError(key)

    def set_config(self, key: str, value: str):
        # TODO: Below Code only works for Notification Priority
        with open(self.path, "r+") as f:
            data = json.load(f)
            data[key] = value
            f.seek(0)
            json.dump(data, f, indent=4)


def get_default_session_data():
    try:
        conf = Config(get_default_session_data=True).get_config(DEFAULT_SESSION_DATA)
        return conf["tag"], conf["name"]
    except (errors.InvalidConfigKeyError, KeyError):
        return default_session_data["tag"], default_session_data["name"]
