import logging
import os
import sys

from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="DEBUG", format=FORMAT, datefmt="[%X]", handlers=[
        RichHandler(rich_tracebacks=True)
    ]
)

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from .controller.Field import Field
from .controller.ConfigNode import ConfigNode