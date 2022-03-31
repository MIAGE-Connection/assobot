import json
import sys
from pathlib import Path

import discord
from discord.ext import commands
from flask import Flask
from zenora import APIClient

from .config import *

sys.dont_write_bytecode = True

APP = Flask(__name__)
BOT = commands.Bot(command_prefix='>', intents=discord.Intents.all())
CLIENT = APIClient(BOT_SECRET, client_secret=CLIENT_SECRET)

@BOT.event
async def on_connect():
    print("The BOT have started !")

def get_or_create_folder_path(path : Path) -> Path:
    if not path.exists():
        path.mkdir()
    return path

def get_or_create_file_path(path: Path) -> Path:
    if not path.exists():
        path.touch()
    return path

def get_or_create_json_file_path(path: Path) -> Path:
    if not path.exists():
        with open(path, 'w') as wtr:
            json.dump(dict(), wtr)
    return path

ASSOBOT_FOLDER = get_or_create_folder_path(Path().home() / '.assobot')
ASSOBOT_SETTINGS_FILE = get_or_create_json_file_path(ASSOBOT_FOLDER / 'settings.json')
ASSOBOT_PLUGIN_SETTING_FOLDER = get_or_create_folder_path(ASSOBOT_FOLDER / 'setting-plugin')

from assobot.core.settings.settings_manager import SettingManager

TMP_FOLDER_PLUGIN = get_or_create_folder_path(ASSOBOT_FOLDER / 'tmp-plugin')
PLUGIN_FOLDER = get_or_create_folder_path(Path(__file__).parent / 'plugins')

STATIC_FOLDER = get_or_create_folder_path(Path(__file__).parent / 'static')
STATIC_DEFAULT_FOLDER = get_or_create_folder_path(STATIC_FOLDER / 'default')
STATIC_PLUGIN_FOLDER = get_or_create_folder_path(STATIC_FOLDER / 'plugins')

TEMPLATE_FOLDER = get_or_create_folder_path(Path(__file__).parent / 'templates')
TEMPLATE_DEFAULT_FOLDER = get_or_create_folder_path(TEMPLATE_FOLDER / 'default')
TEMPLATE_PLUGIN_FOLDER = get_or_create_folder_path(TEMPLATE_FOLDER / 'plugins')

SOURCE_PLUGIN_FOLDER = get_or_create_folder_path(Path(__file__).parent / 'plugins')

APP_SETTINGS_MANAGER = SettingManager(ASSOBOT_SETTINGS_FILE)
APP_SETTINGS_MANAGER.save()
