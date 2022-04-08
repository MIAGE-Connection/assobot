class AuthContext:

    def __init__(self, user, guild = None) -> None:
        self.__user = user
        self.__guild = guild

    @property
    def user(self):
        return self.__user

    @property
    def guild(self):
        return self.__guild

    @guild.setter
    def guild(self, nguild):
        self.__guild = nguild