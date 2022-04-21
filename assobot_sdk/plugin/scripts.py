import shutil
from pathlib import Path

from assobot import ASSOBOT_FOLDER, SOURCE_PLUGIN_FOLDER, STATIC_PLUGIN_FOLDER, TEMPLATE_PLUGIN_FOLDER


__all__ = ['create_plugin', 'build_plugin']

PLUGIN_TEMPLATE_FOLDER = Path(__file__).parent / 'plugin_template'
DIST_FOLDER = Path().cwd() / 'dist'


def replace_tokens_in_ligne(tokens, line):
    for token, value in tokens.items():
        if token in line:
            line = line.replace(token, value)
    return line


def create_plugin(plugin_path : str):
    print("\n")
    print("This command will guide you throught create your Assobot Plugin.")
    print("\n")

    plugin_data = dict()

    plugin_data['[[PLUGIN_NAME]]'] = input('Plugin name : ')
    plugin_data['[[PLUGIN_DESCRIPTION]]'] = input('Description : ')

    print("\n")
    result = input('Do you confirm generation (yes/no) : ')
    print("\n")

    if result not in ['y', 'yes', 'Yes', 'YES']:
        print('Error : Generation aborted')
        return

    current_dir = Path(plugin_path)
    plugin_dir = current_dir / plugin_data['[[PLUGIN_NAME]]'].lower()

    if not plugin_dir.exists():
        plugin_dir.mkdir()

    shutil.copytree(PLUGIN_TEMPLATE_FOLDER, plugin_dir, dirs_exist_ok=True)

    plugin_file = plugin_dir / 'plugin.py'

    with open(plugin_file, 'r') as rdr:
        lines = rdr.readlines()

    with open(plugin_file, 'w') as wtr:
        for line in lines:
            wtr.write(replace_tokens_in_ligne(plugin_data, line))

    print("\n")
    print("Info : Plugin correctly generated !")


def build_plugin(plugin_path : str):
    plugin_path_object = Path(plugin_path)
    
    if not plugin_path_object.exists():
        print(f"Error : {plugin_path} doesn't exist !")
        return

    dist_folder = plugin_path_object.parent / 'dist'

    if not dist_folder.exists():
        dist_folder.mkdir()

    current_dir = Path.cwd()
    plugin_name = f"{plugin_path_object.name}"

    result_path = shutil.make_archive(str(dist_folder/plugin_name), 'zip', plugin_path_object)

    if Path(result_path).exists():
        print("Info : Plugin correctly packaged !")

def __clean_folder(folder) -> None:
    if folder.exists():
        shutil.rmtree(folder)
    folder.mkdir()

def clean_plugins() -> None:
    __clean_folder(TEMPLATE_PLUGIN_FOLDER)
    __clean_folder(STATIC_PLUGIN_FOLDER)
    __clean_folder(SOURCE_PLUGIN_FOLDER)

    __clean_folder(ASSOBOT_FOLDER)

    INIT_FILE = SOURCE_PLUGIN_FOLDER / '__init__.py'

    INIT_FILE.touch()