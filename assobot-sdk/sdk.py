from argparse import *
import argparse

from .plugin import create_plugin

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('--create-plugin', help='Create plugin for assobot', action='store_true')

    args = parser.parse_args()

    if args.create_plugin:
        create_plugin()