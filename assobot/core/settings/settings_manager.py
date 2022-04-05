import json
from pathlib import Path
from ..utils import get_logger

from assobot import SOURCE_PLUGIN_FOLDER, ASSOBOT_PLUGIN_SETTING_FOLDER

LOGGER = get_logger(__name__)

__all__ = ['SettingManager']

class SettingManager:

    def __init__(self, default_setting_path, user_setting_path) -> None:
        self.__settings = dict()
        self.__default_setting_path = default_setting_path
        self.__user_setting_path = user_setting_path
        self.load()

    def get(self, key):
        if self.__settings.get(key, None) is None:
            return "[[UNKNOWN SETTINGS]]"
        
        return self.__settings[key]
    
    def add(self, key : str, value):
        self.__settings[key] = value

    def update(self, data : dict) -> None:
        LOGGER.info("Update of plugin settings")
        for key in data:
            if self.__settings.__contains__(key):
                self.__settings[key] = data[key][0]
        self.save()

    def load(self):
        if not self.__default_setting_path.exists():
            LOGGER.info(f'Creation {self.__default_setting_path} file')
            self.__default_setting_path.touch()

        with open(self.__default_setting_path, 'r') as settings_file:
            LOGGER.info(f"Reading of {self.__default_setting_path} settings file")
            self.__settings.update(json.load(settings_file))

        with open(self.__user_setting_path, 'r') as settings_file:
            LOGGER.info(f"Reading of {self.__user_setting_path} settings file")
            self.__settings.update(json.load(settings_file))

    
    def save(self):
        with open(self.__user_setting_path, 'w+') as settings_file:
            LOGGER.info(f"Writing of {self.__user_setting_path} settings file")      
            json.dump(self.__settings, settings_file)