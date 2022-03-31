import uuid
import logging

from pathlib import Path

from assobot import ASSOBOT_FOLDER

__all__ = ['get_logger']

ASSOBOT_LOG_FILE = ASSOBOT_FOLDER / '.logs'

logging.basicConfig(filename=ASSOBOT_LOG_FILE, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

def get_logger(name : str = str(uuid.uuid4())):
    return logging.getLogger(name)