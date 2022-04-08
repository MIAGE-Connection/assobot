from assobot import BOT, ASSOBOT_GUILDS_FOLDER, get_or_create_folder_path, get_or_create_json_file_path

class Guild:

    def __init__(self, zenora_guild) -> None:
        self.__id = zenora_guild.id
        self.__name = zenora_guild.name
        self.__icon_url = zenora_guild.icon_url
        self.__init_guild_folder()

    def __init_guild_folder(self):
        if self.is_bot_member():
            guild_folder = get_or_create_folder_path(ASSOBOT_GUILDS_FOLDER / self.name.lower().replace(' ', '_'))
            get_or_create_folder_path(guild_folder / 'plugins')
            get_or_create_json_file_path(guild_folder / 'settings.json')

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def icon_url(self):
        return self.__icon_url
        
    def is_bot_member(self):
        guild = BOT.get_guild(self.__id)
        return guild and guild.members