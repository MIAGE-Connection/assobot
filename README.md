# AssoBot

## Getting Started with development

### Windows 

#### Step 1: Get the source code

> You need SSH Keys configured in order to be allowed to clone the repository

```bash
git clone git@github.com:MIAGE-Connection/assobot.git
```

### Step 2: Install Python and pip 

* Install Python (3.8.13) from [here](https://www.python.org/downloads/release/python-3911/)

> Don't forget to add Python to your PATH variable.

* Upgrade pip to it latest version 

```powershell
pip install --upgrade pip
```

### Step 3: Install your build environment

* Install Poetry in order to handle dependancy management and app building.

#### OSX / Linux / BashOnWindows install commands

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```
#### Windows powershell install instructions

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
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