import json
from pathlib import Path
from ..utils import get_logger

from assobot import SOURCE_PLUGIN_FOLDER, ASSOBOT_PLUGIN_SETTING_FOLDER, get_or_create_json_file_path

LOGGER = get_logger(__name__)

__all__ = ['SettingManager']

class SettingManager:

    def __init__(self, settings_path) -> None:
        self.__settings = dict()
        self.__settings_path = settings_path
        self.load()

    def get(self, key):
        if self.__settings.get(key, None) is None:
            return "[[UNKNOWN SETTINGS]]"
        
        return self.__settings[key]

    def set(self, key, value):
        if self.__settings.get(key, None) is None: return
        self.__settings[key] = value
        self.save()

    def add(self, key : str, value):
        self.__settings[key] = value

    def update(self, data : dict) -> None:
        LOGGER.info("Update of plugin settings")
        for key in data:
            self.__settings[key] = data[key][0]
        self.save()

    def load(self):
        with open(self.__settings_path, 'r') as user_settings_file:
            LOGGER.info(f"Reading of {self.__settings_path} settings file")
            self.__settings.update(json.load(user_settings_file))

    def save(self):
        with open(self.__settings_path, 'w+') as settings_file:
            LOGGER.info(f"Writing of {self.__settings_path} settings file")      
            json.dump(self.__settings, settings_file)