# AssoBot

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

### Step 5 : Run app

* Test App launching

```python
poetry run launch-bot
```

## Create your first plugin

In order to create your first assobot plugin you can use the assobot-sdk. This SDK contains various scripts that handle creation, package, etc for Assobot plugin.

### Create a plugin

In order to create your plugin you should use the command below.

```bash
poetry run assobot-sdk --create-plugin ./
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

## Build your plugin

When your plugin is ready, you can build it thanks to the command below.

```
poetry run assobot-sdk --build-plugin <path_to_your_plugin_folder>
```
Then you will find a **dist** folder with inside a file which looks like something like : **<plugin_name>-0.0.0.zip**. 

Finally you can install this plugin web interface of the AssoBot.
