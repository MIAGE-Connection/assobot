
from discord import TextChannel

from assobot import BOT, ASSOBOT_GUILDS_FOLDER, NAME_OF_BOT, PLUGIN_FACTORY, get_or_create_folder_path, get_or_create_json_file_path
from assobot.core.settings import SettingManager

class Guild:

    def __init__(self, zenora_guild) -> None:
        self.__id = zenora_guild.id
        self.__name = zenora_guild.name
        self.__icon_url = zenora_guild.icon_url
        self.__plugins = dict()
        self.__discord_guild = BOT.get_guild(self.id)
        self.__init_guild_folder()

    def __init_guild_folder(self):
        if self.is_bot_member():
            self.__guild_folder =  get_or_create_folder_path(ASSOBOT_GUILDS_FOLDER / self.name.lower().replace(' ', '_'))
            plugins_folder = get_or_create_folder_path(self.__guild_folder / 'plugins')
            get_or_create_json_file_path(self.__guild_folder / 'settings.json')
            for file in plugins_folder.iterdir():
                if file.is_file():
                    self.add_plugin(PLUGIN_FACTORY.get_plugin(file.name.split('-')[0]))

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def icon_url(self):
        return self.__icon_url

    @property
    def plugins(self):
        return self.__plugins

    @property
    def discord_guild(self):
        return self.__discord_guild

    @property
    def plugin_list(self):
        return list(self.__plugins.values())

    def is_bot_member(self):
        guild = BOT.get_guild(self.__id)
        return guild and guild.members

    def add_plugin(self, plugin):
        self.__plugins[plugin.id] = plugin
        plugin.init_settings(self.name)

    def remove_plugin(self, plugin):
        self.__plugins.pop(plugin.id)
        plugin.remove_settings(self.name)

    def get_plugin_settings(self, plugin_name):
        guild_formatted_name = self.__name.lower().replace(' ', '_')
        return SettingManager(ASSOBOT_GUILDS_FOLDER / guild_formatted_name / f"{plugin_name.lower()}-settings.json")

    def get_all_channels(self):
        guild_channels = list()
        for channel in BOT.get_all_channels():
            if channel.guild.id == self.__id:
                guild_channels.append(channel)
        return guild_channels

    def get_text_channels(self):
        guild_channels = list()
        for channel in BOT.get_all_channels():
            if isinstance(channel, TextChannel) and channel.guild.id == self.__id:
                guild_channels.append(channel)
        return guild_channels

    def get_roles(self):
        return self.discord_guild.roles

    def get_assignables_roles(self):
        assignable_roles = []
        for role in self.discord_guild.roles:
            if role.name == NAME_OF_BOT:
                return assignable_roles
            else:
                assignable_roles.append(role)
        return assignable_roles

    def get_reactions(self):
        return self.discord_guild.emojis