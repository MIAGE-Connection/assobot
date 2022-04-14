# AssoBot




### Create and add plugin

#### Create
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

/!\ Attention /!\
You can not have two function with the same name, event beteween two different plugin.

#### Add
Now that your plugin is ready,  you can build it thanks to the command below.

```
poetry run assobot-sdk --build-plugin <path_to_your_plugin_folder>
```
Then you will find a **dist** folder with inside a file which looks like something like : **<plugin_name>-0.0.0.zip**. 

Finally you can install this plugin web interface of the AssoBot.


### Add parameters
if you want to add parameters to your plugin, you can go to the file **settings.json** .

### Update parameters 
Then to update this parameters, you can do it by the web interface of the AssoBot, on the part "configurer".
On the interface, you can personalize your setting or even choose the channel.