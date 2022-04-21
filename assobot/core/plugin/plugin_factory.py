import importlib
import shutil
import zipfile
import subprocess
from pathlib import Path

from assobot import BOT, ASSOBOT_PLUGIN_TEMP_FOLDER, PLUGIN_FOLDER, STATIC_PLUGIN_FOLDER, TEMPLATE_PLUGIN_FOLDER
from assobot.core.utils.file_utils import copy_and_overwrite
from assobot.core.utils.logger import get_logger

LOGGER = get_logger(__name__)

class PluginFactory:

    def __init__(self) -> None:
        self.__plugins = dict()
        self.__load_plugins()

    def install_plugin(self, plugin_path : Path) -> None:
        LOGGER.info(f"Load plugin from {plugin_path}")
        plugin_name = self.__get_plugin_name(plugin_path)
        if not self.__plugins.__contains__(plugin_name):
            self.__clean_tmp_folder()
            self.__extract_to_tmp_folder(plugin_name, plugin_path)
            self.__copy_to_plugin_folder(plugin_name)
            self.__install_dependencies(plugin_name)
            plugin = self.__add_plugin(plugin_name)
            self.__clean_tmp_folder()
        else:
            plugin = self.__plugins[plugin_name]
        return plugin

    def get_plugin(self, plugin_name):
        return self.__plugins[plugin_name]
        
    def __load_plugins(self):
        for file in PLUGIN_FOLDER.iterdir():
            if file.is_dir():
                self.__add_plugin(file.name)

    def __get_plugin_name(self, plugin_path : Path) -> str:
        return plugin_path.stem
        
    def __extract_to_tmp_folder(self, plugin_name : str, plugin_path : Path) -> None:
        if not plugin_path.exists():
            LOGGER.error(f"Plugin file doesn't exist ({plugin_path})")
            return
        
        plugin_tmp_folder = ASSOBOT_PLUGIN_TEMP_FOLDER / plugin_name

        LOGGER.info("Extract plugin files")
        with zipfile.ZipFile(plugin_path, 'r') as zip_ref:
            zip_ref.extractall(plugin_tmp_folder)

    def __copy_to_plugin_folder(self, plugin_name : str) -> None:
        plugin_tmp_folder = ASSOBOT_PLUGIN_TEMP_FOLDER / plugin_name

        templates_tmp_plugin_folder = plugin_tmp_folder / 'templates'
        templates_plugin_folder = TEMPLATE_PLUGIN_FOLDER / plugin_name

        static_tmp_plugin_folder = plugin_tmp_folder / 'static'
        static_plugin_folder = STATIC_PLUGIN_FOLDER / plugin_name

        source_tmp_plugin_folder = ASSOBOT_PLUGIN_TEMP_FOLDER / plugin_name
        source_plugin_folder = PLUGIN_FOLDER / plugin_name
        if not source_plugin_folder.exists(): source_plugin_folder.mkdir()

        source_core_tmp_plugin_folder = plugin_tmp_folder / 'core'
        source_core_plugin_folder = PLUGIN_FOLDER / plugin_name / 'core'

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

    def __add_plugin(self, plugin_name) -> None:
        module = importlib.import_module(f"assobot.plugins.{plugin_name}.plugin")
        plugin_class = getattr(module, f"{plugin_name}Plugin")
        plugin = plugin_class()
        self.__plugins[plugin_name] = plugin
        BOT.add_cog(plugin)
        return plugin
    
    def __clean_tmp_folder() -> None:
        if ASSOBOT_PLUGIN_TEMP_FOLDER.exists():
            ASSOBOT_PLUGIN_TEMP_FOLDER.rmtree()
        ASSOBOT_PLUGIN_TEMP_FOLDER.mkdir()