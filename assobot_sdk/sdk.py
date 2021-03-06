from argparse import *
import argparse
import pathlib

from assobot_sdk.plugin.scripts import clean_plugins

from .plugin import create_plugin, build_plugin

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('--create-plugin', help='Create plugin for assobot', action='store_true')
    parser.add_argument('--build-plugin', help='Build assobot plugin from folder', action='store_true')
    parser.add_argument('--clean-plugins', help='Clean assobot\'s plugins', action='store_true')
    parser.add_argument('plugin_path', help='Give the plugin path', nargs="?", default='.', type=pathlib.Path)

    args = parser.parse_args()

    if args.create_plugin:
        create_plugin(args.plugin_path)
        return
    
    if args.build_plugin:
        build_plugin(args.plugin_path)
        return

    if args.clean_plugins:
        clean_plugins()
        return