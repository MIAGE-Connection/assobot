import imp
import sys
from pathlib import Path

sys.dont_write_bytecode = True

ASSOBOT_FOLDER = Path().home() / '.assobot'

if not ASSOBOT_FOLDER.exists():
    ASSOBOT_FOLDER.mkdir()
