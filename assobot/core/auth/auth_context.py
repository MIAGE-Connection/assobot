from assobot.core.plugin.plugin_manager import PluginManager

class AuthContext:

    def __init__(self, user, guild = None) -> None:
        self.__user = user
        self.__guild = guild
        self.__plugin_manager = None if guild is None else PluginManager(guild)

    @property
    def user(self):
        return self.__user

    @property
    def guild(self):
        return self.__guild

    @guild.setter
    def guild(self, nguild):
        self.__guild = nguild
        if self.__plugin_manager is not None:
            self.__plugin_manager.reset()
        self.__plugin_manager = None if nguild is None else PluginManager(nguild)

    @property
    def plugin_manager(self):
        return self.__plugin_manager