import os
import json

import flomo.errors as errors
import flomo.helpers as helpers


class Config:
    def __init__(self, initializing: bool = False):
        self.path = helpers.get_path("config.json", in_data=True)

        if not initializing and not self._config_file_exists():
            raise errors.NoConfigError()

    def _config_file_exists(self):
        return os.path.exists(self.path)  # TODO: Check if file contents are proper.

    def create_config(self):
        if self._config_file_exists():
            return

        with open(self.path, "w") as f:
            data = {
                "default_session_data": {
                    "tag": "Work",
                    "name": "Working",
                },
                "notification_priority": "normal",
                "tag_colors": {"Work": "blue", "Study": "red", "Exercise": "green"},
            }

            json.dump(data, f, indent=4)