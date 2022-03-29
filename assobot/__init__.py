import imp
import sys
from pathlib import Path

sys.dont_write_bytecode = True

def get_or_create_folder_path(path : Path) -> Path:
    if not path.exists():
        path.mkdir()
    return path


ASSOBOT_FOLDER = get_or_create_folder_path(Path().home() / '.assobot')

TMP_FOLDER_PLUGIN = get_or_create_folder_path(ASSOBOT_FOLDER / 'tmp-plugin')
PLUGIN_FOLDER = get_or_create_folder_path(Path.cwd() / 'assobot' / 'plugins')

STATIC_FOLDER = get_or_create_folder_path(Path.cwd() / 'assobot' / 'static')
STATIC_DEFAULT_FOLDER = get_or_create_folder_path(STATIC_FOLDER / 'default')
STATIC_PLUGIN_FOLDER = get_or_create_folder_path(STATIC_FOLDER / 'plugins')

TEMPLATE_FOLDER = get_or_create_folder_path(Path.cwd() / 'assobot' / 'templates')
TEMPLATE_DEFAULT_FOLDER = get_or_create_folder_path(TEMPLATE_FOLDER / 'default')
TEMPLATE_PLUGIN_FOLDER = get_or_create_folder_path(TEMPLATE_FOLDER / 'plugins')

