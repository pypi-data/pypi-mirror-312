from pathlib import Path
from typing import Final

COLT_TYPEKEY: Final = "type"
COLT_ARGSKEY: Final = "*"

DEFAULT_WORKING_DIRECTORY: Final = Path.cwd()
DEFAULT_MLFACTORY_DIRECTORY: Final = DEFAULT_WORKING_DIRECTORY / ".harbory"
DEFAULT_MLFACTORY_SETTINGS_PATH: Final = DEFAULT_WORKING_DIRECTORY / "harbory.yml"
