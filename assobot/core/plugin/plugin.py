import uuid

from assobot import STATIC_PLUGIN_FOLDER, TEMPLATE_PLUGIN_FOLDER

__all__ = ['AbstractPlugin']

class AbstractPlugin:

    def __init__(self, name, description) -> None:
        self.__id = uuid.uuid4()
        self.__enabled = False
        self.__name = name
        self.__description = description
        self.__static_folder = STATIC_PLUGIN_FOLDER / self.__name.lower()
        self.__templates_folder = TEMPLATE_PLUGIN_FOLDER / self.__name.lower()

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

    def __str__(self) -> str:
        return f"<{self.id}> - {self.name}"