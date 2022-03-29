import shutil
from pathlib import Path

__all__ = ['create_plugin']

PLUGIN_TEMPLATE_FOLDER = Path(__file__).parent / 'plugin_template'

def replace_tokens_in_ligne(tokens, line):
    for token, value in tokens.items():
        if token in line:
            line = line.replace(token, value)
    return line

def create_plugin():
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
        return

    current_dir = Path.cwd()
    plugin_dir = current_dir / plugin_data['[[PLUGIN_NAME]]'].lower()

    if not plugin_dir.exists():
        plugin_dir.mkdir()

    shutil.copytree(PLUGIN_TEMPLATE_FOLDER, plugin_dir, dirs_exist_ok=True)

    plugin_file = plugin_dir /'plugin.py'

    with open(plugin_file, 'r') as rdr:
        lines = rdr.readlines()
    
    with open(plugin_file, 'w') as wtr:
        for line in lines:
            wtr.write(replace_tokens_in_ligne(plugin_data, line))
    
    print("\n")
    print("Plugin correctly generated !")

    
