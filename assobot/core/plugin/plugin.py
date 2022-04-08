import os
import uuid
import shutil
from assobot.core.plugin import plugin_factory

from discord.ext import commands

from assobot import ASSOBOT_GUILDS_FOLDER, AUTH_MANAGER, BOT, PLUGIN_FOLDER, STATIC_PLUGIN_FOLDER, TEMPLATE_PLUGIN_FOLDER
from assobot.core.settings.settings_manager import SettingManager

__all__ = ['AbstractPlugin']

class AbstractPlugin(commands.Cog):

    def __init__(self, name, description) -> None:
        self.__id = uuid.uuid4()
        self.__bot = BOT
        self.__enabled = True
        self.__name = name
        self.__description = description
        self.__static_folder = STATIC_PLUGIN_FOLDER /self.__name.lower()
        self.__templates_folder = TEMPLATE_PLUGIN_FOLDER / self.__name.lower()
        self.__default_settings_file = PLUGIN_FOLDER / self.name.lower() / 'settings.json'

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
    def enabled(self, guild = None):
        return bool(self.get_settings_manager(guild).get('enabled'))

    def get_settings_manager(self, guild = None):
        if guild is None:
            guild = AUTH_MANAGER.get_current_ctx().guild

        guild_name_formatted = guild.name.lower().replace(' ', '_')
        plugin_user_settings = ASSOBOT_GUILDS_FOLDER / guild_name_formatted / 'plugins' / f"{self.name.lower()}-settings.json"
        return SettingManager(plugin_user_settings)

    @property
    def bot(self):
        return self.__bot

    def init_settings(self, guild_name):
        guild_name_formatted = guild_name.lower().replace(' ', '_')
        plugin_user_settings = ASSOBOT_GUILDS_FOLDER / guild_name_formatted / 'plugins' / f"{self.name.lower()}-settings.json"
        if not plugin_user_settings.exists():
            shutil.copy(self.__default_settings_file, plugin_user_settings)

    def remove_settings(self, guild_name):
        guild_name_formatted = guild_name.lower().replace(' ', '_')
        plugin_user_settings = ASSOBOT_GUILDS_FOLDER / guild_name_formatted / 'plugins' / f"{self.name.lower()}-settings.json"
        if plugin_user_settings.exists():
            os.remove(plugin_user_settings)

    def __str__(self) -> str:
        return f"<{self.id}> - {self.name}"