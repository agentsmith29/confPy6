import logging
import os
import sys

from rich.logging import RichHandler
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from .controller.Field import Field
from .controller.ConfigNode import ConfigNode