# ConfigHandler

## Description
This module is used to handle configuration files for flexsensor.
It hgas been designed, so the user can create a config with an UI, automatically connected to the signal and slots.

## Requirements
Install the requirements with pip:
```python
pip install pyside6, rich, pyyaml
````
## Usage
The Usage is straight forward. Just create a new ```ConfigNode``` object and call the show() method.
```python

class ApplicationConfig(ConfigNode):

    def __init__(self) -> None:
        # Call the base class (important!)
        super().__init__()

        # Some fields
        self.output_directory: Field[Path] = Field(Path("C:\\{wafer_nr}"))
        self.wafer_version: Field[str] = Field("v1.0")
        self.wafer_number: Field[int] = Field(1)
        # A field with an description
        self.wafer_nr: Field[str] = Field("12345ABCD_{wafer_number}",
                                          friendly_name="Wafer Number",
                                          description="The version of the wafer")
        # Some other fields
        self.my_tuple: Field[tuple] = Field((1,2))
        self.any_list: Field[list] = Field([1, 2])
        
        # Even a nested config is possible
        self.other_config: OtherConfig = OtherConfig()

        # Don't forget to register the fields (important!)
        self.register()
```