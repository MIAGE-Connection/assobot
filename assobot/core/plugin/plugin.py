import uuid

from discord.ext import commands

from assobot import BOT, SOURCE_PLUGIN_FOLDER, STATIC_PLUGIN_FOLDER, TEMPLATE_PLUGIN_FOLDER
from assobot.core.settings.settings_manager import SettingManager

__all__ = ['AbstractPlugin']

class AbstractPlugin(commands.Cog):

    def __init__(self, name, description) -> None:
        self.__id = uuid.uuid4()
        self.__bot = BOT
        self.__enabled = True
        self.__name = name
        self.__description = description
        self.__static_folder = STATIC_PLUGIN_FOLDER / self.__name.lower()
        self.__templates_folder = TEMPLATE_PLUGIN_FOLDER / self.__name.lower()
        self.__settings = SettingManager(SOURCE_PLUGIN_FOLDER / self.__name.lower() / 'settings.json')

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def namespace(self):
        return self.__name.lower()

    @property
    def description(self):
        return self.__description
    
    @property
    def static_folder(self):
        return self.__static_folder
    
    @property
    def templates_folder(self):
        return self.__templates_folder

    @property
    def enabled(self):
        return self.__enabled

    @enabled.setter
    def enabled(self, value):
        self.__enabled = value

    @property
    def settings(self):
        return self.__settings

    @property
    def bot(self):
        return self.__bot

    def __str__(self) -> str:
        return f"<{self.id}> - {self.name}"