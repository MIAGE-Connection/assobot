import json
from pathlib import Path
from ..utils import get_logger

LOGGER = get_logger(__name__)

__all__ = ['SettingManager']

class Setting:

    def __init__(self, name : str, value) -> None:
        self.__n = name
        self.__v = value
    
    @property
    def name(self):
        return self.__n

    @property
    def value(self):
        return self.__v
    
    @value.setter
    def value(self, n_value):
        self.__v = n_value

class SettingManager:

    def __init__(self, setting_path) -> None:
        self.__settings = dict()
        self.__setting_path = Path(setting_path)
        self.load()

    def get(self, key) -> Setting:
        if self.__settings.get(key, None) is None:
            return Setting("Unknown Settings", "[[UNKNOWN SETTINGS]]")
        
        return Setting(key, self.__settings[key])
    
    def add(self, key : str, value):
        self.__settings[key] = value

    def update(self, data : dict) -> None:
        LOGGER.info("Update of plugin settings")
        for key in data:
            if self.__settings.__contains__(key):
                self.__settings[key] = data[key][0]
        self.save()

    def load(self):
        if not self.__setting_path.exists():
            LOGGER.info(f'Creation {self.__setting_path} file')
            self.__setting_path.touch()

        with open(self.__setting_path, 'r') as settings_file:
            LOGGER.info(f"Reading of {self.__setting_path} settings file")
            self.__settings.update(json.load(settings_file))
    
    def save(self):
        with open(self.__setting_path, 'w+') as settings_file:
            LOGGER.info(f"Writing of {self.__setting_path} settings file")      
            json.dump(self.__settings, settings_file)