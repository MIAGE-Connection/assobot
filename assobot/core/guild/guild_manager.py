from assobot.core.guild import Guild

class GuildManager:

    def __init__(self) -> None:
        self.__guilds = dict()

    def get(self, guild_id) -> Guild:
        if self.__guilds.__contains__(guild_id):
            return self.__guilds[guild_id]
        raise Exception("You are not administrator of this guild")

    def add(self, zen_guild) -> None:
        if not self.__guilds.__contains__(zen_guild.id):
            guild = Guild(zen_guild)
            self.__guilds[zen_guild.id] = guild

    @property
    def guilds(self):
        return list(self.__guilds.values())