# AssoBot

[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)


## Authors

- [@Ni-g-3l](https://www.github.com/Ni-g-3l)
- [@shapeqs](https://www.github.com/shapeqs)
- [@oreLINK](https://www.github.com/oreLINK)
- [@Baptiste-crypto](https://www.github.com/Baptiste-crypto)
- [@dawencalippe](https://www.github.com/dawencalippe)
- [@yelhaddady](https://www.github.com/yelhaddady)
- [@auroreGm](https://www.github.com/auroreGm)


## Getting Started with development

### Step 1: Get the source code

> You need SSH Keys configured in order to be allowed to clone the repository

```bash
git clone git@github.com:MIAGE-Connection/assobot.git
```

### Step 2: Install Python and pip 

* Install Python (3.8.13) from [here](https://www.python.org/downloads/release/python-3813/)

> Don't forget to add Python to your PATH variable.

* Upgrade pip to it latest version 

```powershell
pip install --upgrade pip
```

### Step 3: Install your build environment

* Install Poetry in order to handle dependancy management and app building.

```powershell
pip install poetry
```

### Step 4: Install app

* Go into project folder

* Install App environment 

```powershell
poetry install
```

### Step 5 : Refere to [Environment Variables and secret.py file](#environment-variables-and-secret.py-file)

### Step 6 : Run app

* Test App launching

```python
poetry run launch_bot
```

## Project development

### FrontEnd

In order to simplify the development of new page for the website we decided to use de micro framework CSS PicoCSS. 

* [Website](https://picocss.com)
* [Documentation](https://picocss.com/docs/)

### Backend

#### Route 

All route are initialized in python package ***assobot.core.package.route***, and each functionnal domain has it own file (plugin, guild, etc..)

#### File Structure

The project is composed of 2 project :

- Assobot (Discord Bot and WebServer)
- Assobot-sdk (CLI and plugin tools)
- Assobot-plugin (Source code of default plugins)

#### Assobot

The Assobot project contains many folders and files :
- core (source code of the project)
- plugins (install folder of all assobot plugin)
- static/default (resources files of default website)
- static/plugins (resources files of plugins)
- templates/default (HTML file of default website)
- templates/plugins (HTML file of plugins)

> For ***static*** and ***templates*** each plugin has it's own folder.

#### Assobot-sdk

The SDK project contains many folders and files :
- plugin/plugin_template (template used to initialise new plugin)
- plugin/plugin_default (folder which contains source code of default plugin like '**WelcomePlugin**')

## Plugin development

In order to create your first assobot plugin you can use the assobot-sdk. This SDK contains various scripts that handle creation, package, etc for Assobot plugin.

### Create a plugin

In order to create your plugin you should use the command below.

```bash
poetry run assobot_sdk --create-plugin <path_of_the_destination>
```

Then, you just have to follow instructions in your terminal. 

Finally, you will get a new folder which contains your plugin. The folder structure of the plugin is very easy. 

```
- root : <plugin_name>
    - core   : main python package of your plugin
    - static : folder which contains static resources used by the the web interface
    - templates : the web interface main page
    - __init__.py : file used to initialise python package
    - plugin.py : file used to connect Assobot to your plugin
```

If you want add features you can code into the **core** folder and call it from the file **plugin.py**

### Build your plugin

When your plugin is ready, you can build it thanks to the command below.

```
poetry run assobot_sdk --build-plugin <path_to_your_plugin_folder>
```
Then you will find a **dist** folder with inside a file which looks like something like : **<plugin_name>.zip**. 

Finally you can install this plugin web interface of the AssoBot.

## Environment Variables and secret.py file

To run this project, you will need to create a ```secret.py``` in the root of the assobot module.

You can copy/paste this code into the file and then fill it with you personnal tokens.

```python
BOT_SECRET='<your_personal_token_here>'
CLIENT_SECRET='<your_personal_token_here>'
```

## Socials

<center>

[![Facebook](https://img.shields.io/twitter/url?color=232374E1&label=Facebook&logo=Facebook&logoColor=%232374E1&style=for-the-badge&url=https%3A%2F%2Fwww.facebook.com%2Fmiageconnection%2F)](https://www.facebook.com/miageconnection)
[![Instagram](https://img.shields.io/twitter/url?color=232374E1&label=Instagram&logo=instagram&style=for-the-badge&url=https%3A%2F%2Fwww.instagram.com%2Fmiageconnection)](https://www.instagram.com/miageconnection/)
[![Twitter](https://img.shields.io/twitter/url?color=232374E1&label=Twitter&logo=twitter&style=for-the-badge&url=https%3A%2F%2Ftwitter.com%2Fmiageconnection)](https://twitter.com/MIAGEConnection)

</center>