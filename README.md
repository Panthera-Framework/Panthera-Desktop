Panthera-Desktop
================

A very simple desktop framework that includes basic classes required for every desktop application (configuration etc.)

## Requirements

- Python 2.7 or Python 3
- [ArgsParse](https://docs.python.org/dev/library/argparse.html)
- (Optional) PySide or PyQT4 for Qt based GUI support

## Installation

```bash
cd /tmp
git clone https://github.com/Panthera-Framework/Panthera-Desktop
cd Panthera-Desktop
sudo ./setup.py install
```

## Basic modules

Every included module can be replaced with your own, eg. you can extend existing module and put it instead of old one.

```python
import pantheradesktop.hooking.pantheraHooking

class myLoggingClass(pantheradesktop.hooking.pantheraHooking):
    (...)

kernel.coreClasses['logging'] = myLoggingClass
```

### argsParser

argsParser is a class that uses argsparse module and extends it by adding callback function to every argument.

You should extend this class by creating your own with custom argument handlers.

```python
def version(self, value=''):
        """
            Example argument handler, shows application version
            
        """
    
        print(self.panthera.appName + " " +self.panthera.version)
        sys.exit(0)
```

```python
argsParser.createArgument('--version', argsParser.version, '', 'Display help', action='store_true')
```

Everytime when you will use --version argument there will be a callback function - argsParser.version(data) called with argument data you provided.


### logging

Every application requires a good logging so no error should be impossible to fix. So, this is a very simple module, inside of code only one thing you have to do
is using `self.panthera.logging.output('This is a message', 'module name')`


### config

Configuration file is stored by default in ~/.APPNAME_HERE/config.json, it's written in easy to parse JSON format.
The class provides full read-write support for configuration files.

```python
self.panthera.config.setKey('key', 'value')
self.panthera.config.getKey('non-existing-key', 'put default value if does not exists - this is optional')
self.panthera.config.getKey('key') # return "value", if key does not exists should return None
```
