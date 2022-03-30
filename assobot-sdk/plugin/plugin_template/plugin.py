from assobot.core.plugin import AbstractPlugin
from .core import *

class Plugin(AbstractPlugin):

    def __init__(self) -> None:
        super().__init__('[[PLUGIN_NAME]]', '[[PLUGIN_DESCRIPTION]]')

    def init(self):
        pass