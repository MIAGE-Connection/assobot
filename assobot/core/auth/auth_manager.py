from assobot import APP
from assobot.core.auth import AuthContext
from assobot.core.utils.logger import get_logger

from flask import session

LOGGER = get_logger(__name__)

class AuthManager:

    def __init__(self) -> None:
        self.__auth_manager = dict()
        
    def create_auth(self, user) -> None:
        LOGGER.info('Create new auth')
        self.__auth_manager[user] = AuthContext(user)

    def remove_auth(self, user):
        LOGGER.info('Remove auth')
        if self.__auth_manager.__contains__(user):
            self.__auth_manager.pop(user)
    
    def get(self, user):
        if not self.__auth_manager.__contains__(user):
            raise Exception('No user corresponding')
        return self.__auth_manager[user]

    def get_current_ctx(self):
        return self.__auth_manager[session['token']]