# ConfigHandler

## Description
This module is used to handle configuration files for FlexSensor.
It has been designed, so the user can create a config with a UI, automatically connected to the signal and slots.

## Requirements
Install the requirements with pip:
```bash
pip install -r requirements.txt
````
or
```bash
pip install PySide6 PyYAML rich
```
## Installing this repo to your project using pip
Just add the following line to your requirements.txt
```bash
git+https://github.com/agentsmith29/fstools.confighandler.git@<branch>
# e.g., from branch main
git+https://github.com/agentsmith29/fstools.confighandler.git@<branch>
```
oder directly using pip (without requirements.txt)
```bash
# or manually
pip install git+https://github.com/agentsmith29/fstools.confighandler.git@<branch>
```
## Usage
Example files can be found in `./examples`.
The usage is straight forward. Just create a new ```ConfigNode``` object and call the show() method.
## Field Types
The current implementation supports the following literal field types:
[FieldBool.py](./src/confPy6/controller/fields/FieldBool.py)
[FieldFloat.py](./src/confPy6/controller/fields/FieldFloat.py)
[FieldInt.py](./src/confPy6/controller/fields/FieldInt.py)
[FieldString.py](./src/confPy6/controller/fields/FieldString.py)

The following list types are also supported:
[FieldList.py](./src/confPy6/controller/fields/FieldList.py)
[FieldSelectableList.py](./src/confPy6/controller/fields/FieldSelectableList.py)
[FieldTuple.py](./src/confPy6/controller/fields/FieldTuple.py)

The object pathlib.Path can also be stored:
[FieldPath.py](./src/confPy6/controller/fields/FieldPath.py)

Usually the type is automatically detected.
### Creating a config
Before you can start working with the config, you need to create some kind of sceleton. This
has three advantages:
1. You can define the type of the fields. You can give them friendly names and descriptions.
2. The parsing of the config file is much easier, because the parser knows the type of the fields.
3. When working with this library, you can use the auto completion of your IDE, since it is a class.

```python
import confPy6 as cfg

class SecondConfig(cfg.ConfigNode):

    def __init__(self, enable_log=True) -> None:
        # Call the base class (important!)
        super().__init__(internal_log=enable_log)

        # Create a field of type int. Set a default value, a friendly name and a description
        self.test_int: cfg.Field[int] = cfg.Field(1,
                                                  friendly_name="My Test Int",
                                                  description="This is just an integer")

class ApplicationConfig(cfg.ConfigNode):

    def __init__(self, enable_log=True) -> None:
        # Call the base class (important!)
        super().__init__(internal_log=enable_log)

        # Some fields
        # Create a field of type int. Set a default value, a friendly name and a description
        self.counter: cfg.Field[int] = cfg.Field(
            1, friendly_name="My Counter", description="This is just an integer")

        self.version: cfg.Field[str] = cfg.Field(
            "v1.0", friendly_name="Version", description="The version")

        # You can also omit the friendly name and description
        self.check: cfg.Field[bool] = cfg.Field(False)

        # Some other fields
        # Also possible to create a field of type list
        self.my_tuple: cfg.Field[tuple] = cfg.Field((1, 2))
        self.any_list: cfg.Field[list] = cfg.Field([1, 2])

        # Even a nested config is possible
        self.second_config: SecondConfig = SecondConfig()

        # Don't forget to register the fields (important!)
        self.register()
```

### Loading and saving a config
It is possible to load and save a config. The config is saved as a yaml file.
```python
from ApplicationConfig import ApplicationConfig

if __name__ == "__main__":
    config = ApplicationConfig(enable_log=True)
    config.save('./configs/ApplicationConfig.yaml')
    config.load('./configs/ApplicationConfig.yaml')
```

### Autosaving
It is also possible to autosave a config. This is useful, if you want to save the config, when the user changes a value.
```python
from ApplicationConfig import ApplicationConfig

if __name__ == "__main__":
    config = ApplicationConfig(enable_log=True)
    config.autosave(enable=True, path='./configs_autosave')
```

### Creating a UI
The condifg handler build an UI in the background. You can access the widget using
```python
import logging
import sys

from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTreeWidget

from ApplicationConfig import ApplicationConfig

if __name__ == "__main__":
    # Creating the UI
    window = QMainWindow()
    wdg = QWidget()
    grd = QtWidgets.QGridLayout()
    wdg.setLayout(grd)

    # Add the config to the UI
    config = ApplicationConfig(enable_log=True)
    conf_view = config.view.widget()
    grd.addWidget(conf_view, 0, 0)

    window.setCentralWidget(wdg)
    window.show()
    sys.exit(app.exec())
```
or using a tree view (which is sometimes more useful)
```python
import logging
import sys

from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTreeWidget

from ApplicationConfig import ApplicationConfig

if __name__ == "__main__":
    # Creating the UI
    window = QMainWindow()
    wdg = QWidget()
    grd = QtWidgets.QGridLayout()
    wdg.setLayout(grd)

    # Add the config to the UI
    config = ApplicationConfig(enable_log=True)
    # Create a tree view
    tree = QTreeWidget()
    tree.setColumnCount(3)
    tree.setHeaderLabels(["Name", "Type", "Description"])
    
    # Get the tree item
    config_item = config.view.ui_tree_widget_item(tree)
    
    tree.addTopLevelItem(config_item)
    grd.addWidget(tree, 2, 0)
    
    window.setCentralWidget(wdg)
    window.show()
    sys.exit(app.exec())
```
## Environment Variables
**confPy6** allows to automatically set environment variables. This can be useful, if you cannot use the already 
initialized class (e.g. you want to retrieve a variable during an import of a module). See (example4)[./examples/example4.py]
```python
class ApplicationConfig(cfg.ConfigNode):

    def __init__(self) -> None:
        super().__init__()

        self.wafer_list: cfg.Field[int] = cfg.Field(1, env_var="WAFER_LIST")
        self.wafer_list2: cfg.Field[int] = cfg.Field(2)

        self.register()
```
use
```python
print(os.environ['WAFER_LIST'])
```
to print the environment variable.
## Troubleshoting
When working inside the examples folder, you need to add the 'confPy6' folder to the python path.
```python
import sys
sys.path.append('../src/')
```

# Citing 
If you use this  code, please cite:
```Schmidt, C. (2024). fstools.confighandler - FlexSensor Tools: Configuration File Handler (Version 1.2.2) [Computer software]. https://github.com/agentsmith29/fstools.confighandler```
or 
```bibtex
@software{Schmidt_fstools_confighandler_-_FlexSensor_2024,
    author = {Schmidt, Christoph},
    month = feb,
    title = {{fstools.confighandler - FlexSensor Tools: Configuration File Handler}},
    url = {https://github.com/agentsmith29/fstools.confighandler},
    version = {1.2.2},
    year = {2024}
}
```
