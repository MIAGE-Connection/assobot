import os
import json
import shutil
import zipfile
import importlib
import subprocess
from pathlib import Path

from assobot import ASSOBOT_PLUGIN_SETTING_FOLDER, BOT, PLUGIN_FOLDER, STATIC_PLUGIN_FOLDER, TEMPLATE_PLUGIN_FOLDER, ASSOBOT_PLUGIN_TEMP_FOLDER
from assobot.core.plugin import AbstractPlugin

from assobot.core.utils import get_logger
from assobot.core.utils.file_utils import copy_and_overwrite

__all__ = ['PluginManager']

LOGGER = get_logger(__name__)

class PluginManager:

    def __init__(self, guild) -> None:
        self.__plugins = dict()
        self.__guild = guild.lower().replace(' ', '_')
        self.__plugins_folder = PLUGIN_FOLDER / self.__guild
        self.__load_plugins()

    @property
    def plugins(self):
        return self.__plugins

    def load_plugin(self, plugin_path : Path) -> None:
        LOGGER.info(f"Load plugin from {plugin_path}")
        plugin_name = self.__get_plugin_name(plugin_path)
        self.__extract_to_tmp_folder(plugin_name, plugin_path)
        self.__copy_to_plugin_folder(plugin_name)
        self.__install_dependencies(plugin_name)
        self.__add_plugin(plugin_name)

    def __load_plugins(self) -> None:
        if not self.__plugins_folder.exists(): self.__plugins_folder.mkdir()
        init_plugins_folder = self.__plugins_folder / '__init__.py'
        if not init_plugins_folder.exists(): init_plugins_folder.touch()

        for file in self.__plugins_folder.iterdir():
            if file.is_dir():
                self.__add_plugin(file.name)

    def __get_plugin_name(self, plugin_path : Path) -> str:
        return plugin_path.name.split('-')[0]
        
    def __extract_to_tmp_folder(self, plugin_name : str, plugin_path : Path) -> None:
        if not plugin_path.exists():
            LOGGER.error(f"Plugin file doesn't exist ({plugin_path})")
            return
        
        plugin_tmp_folder = ASSOBOT_PLUGIN_TEMP_FOLDER / plugin_name

        LOGGER.info("Extract plugin")
        with zipfile.ZipFile(plugin_path, 'r') as zip_ref:
            zip_ref.extractall(plugin_tmp_folder)

    def __copy_to_plugin_folder(self, plugin_name : str) -> None:
        plugin_tmp_folder = ASSOBOT_PLUGIN_TEMP_FOLDER / plugin_name

        templates_tmp_plugin_folder = plugin_tmp_folder / 'templates'
        guild_templates_folder = TEMPLATE_PLUGIN_FOLDER / self.__guild
        if not guild_templates_folder.exists(): guild_templates_folder.mkdir()
        templates_plugin_folder = guild_templates_folder / plugin_name

        static_tmp_plugin_folder = plugin_tmp_folder / 'static'
        guild_static_plugin_folder = STATIC_PLUGIN_FOLDER / self.__guild
        if not guild_static_plugin_folder.exists(): guild_static_plugin_folder.mkdir()
        static_plugin_folder = guild_static_plugin_folder / plugin_name

        source_tmp_plugin_folder = ASSOBOT_PLUGIN_TEMP_FOLDER / plugin_name
        guild_source_plugin_folder = PLUGIN_FOLDER / self.__guild
        if not guild_source_plugin_folder.exists(): guild_source_plugin_folder.mkdir()
        source_plugin_folder = guild_source_plugin_folder / plugin_name

        source_core_tmp_plugin_folder = plugin_tmp_folder / 'core'
        source_core_plugin_folder = guild_source_plugin_folder / plugin_name / 'core'

        guild_settings_plugin_folder = ASSOBOT_PLUGIN_SETTING_FOLDER / plugin_name
        if not guild_settings_plugin_folder.exists(): guild_settings_plugin_folder.mkdir()
        settings_plugin_folder = ASSOBOT_PLUGIN_SETTING_FOLDER / plugin_name

        if not settings_plugin_folder.exists():
            settings_plugin_folder.mkdir()

        settings_plugin_file = settings_plugin_folder / 'settings.json'

        if not settings_plugin_file.exists():
            with open(settings_plugin_file, 'w') as wtr:
                json.dump(dict(), wtr)

        if not source_plugin_folder.exists():
            source_plugin_folder.mkdir()

        LOGGER.info("Copy templates files")
        copy_and_overwrite(templates_tmp_plugin_folder, templates_plugin_folder)
        
        LOGGER.info("Copy static files")
        copy_and_overwrite(static_tmp_plugin_folder, static_plugin_folder)

        LOGGER.info("Copy source files")
        for default_file in ['plugin.py', '__init__.py', 'settings.json']:
            source_tmp_file = source_tmp_plugin_folder / default_file
            source_file = source_plugin_folder / default_file
            shutil.copyfile(source_tmp_file, source_file)

        LOGGER.info("Copy core files")
        copy_and_overwrite(source_core_tmp_plugin_folder, source_core_plugin_folder)

    def __install_dependencies(self, plugin_name : str) -> None:
        plugin_tmp_folder = ASSOBOT_PLUGIN_TEMP_FOLDER / plugin_name
        requirements_file = plugin_tmp_folder / 'requirements.txt'
        if requirements_file.exists():
            subprocess.call(['pip', 'install', '-r', requirements_file])

    def __add_plugin(self, plugin_name : str) -> None:
        module = importlib.import_module(f"assobot.plugins.{self.__guild}.{plugin_name}.plugin")
        plugin_class = getattr(module, f"{plugin_name}Plugin")
        plugin = plugin_class()
        BOT.add_cog(plugin)
        self.__plugins[plugin.id] = plugin

    def unload_plugin(self, plugin : AbstractPlugin) -> None:
        LOGGER.info(f"Remove plugin from {plugin.name}")
        self.__remove_from_plugin_folder(plugin.namespace)
        self.__remove_plugin(plugin)

    def __remove_from_plugin_folder(self, plugin_name : str) -> None:
        templates_plugin_folder = TEMPLATE_PLUGIN_FOLDER / self.__guild / plugin_name
        static_plugin_folder = STATIC_PLUGIN_FOLDER / self.__guild / plugin_name
        source_plugin_folder = PLUGIN_FOLDER / self.__guild / plugin_name

        if not source_plugin_folder.exists():
            source_plugin_folder.mkdir()

        LOGGER.info("Remove templates files")
        shutil.rmtree(templates_plugin_folder)
        
        LOGGER.info("Remove static files")
        shutil.rmtree(static_plugin_folder)

        LOGGER.info("Remove source files")
        shutil.rmtree(source_plugin_folder)

    def __remove_plugin(self, plugin) -> None:
        BOT.remove_cog(f"{plugin.name}Plugin")
        self.__plugins.pop(plugin.id)
