from os import environ

from .utils.helper_functions import load_config
from .utils.schema_manager import (
    _schema_manager,
    behavior,
    experiment,
    mice,
    recording,
    stimulus,
)
# Set version (this needs to be before other imports)
__version__ = "0.0.3"

# Set environment variables
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

# Make commonly used components available at package level
__all__ = ["experiment",
           "stimulus",
           "behavior",
           "recording",
           "mice",
           "load_config",
           "_schema_manager"]
