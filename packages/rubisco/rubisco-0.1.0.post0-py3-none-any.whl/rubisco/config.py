# -*- mode: python -*-
# vi: set ft=python :

# Copyright (C) 2024 The C++ Plus Project.
# This file is part of the Rubisco.
#
# Rubisco is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# Rubisco is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Module configuration."""

from __future__ import annotations

import os
import sys

from rubisco.lib.command import command
from rubisco.lib.pathlib import Path
from rubisco.lib.version import Version

# Application basic configurations.
APP_NAME = "rubisco"
APP_VERSION = Version((0, 1, 0))
MINIMUM_PYTHON_VERSION = (3, 11)

# I18n configurations.
TEXT_DOMAIN = APP_NAME
DEFAULT_CHARSET = "UTF-8"

# Miscellaneous configurations.
TIMEOUT = 15
COPY_BUFSIZE = 1024 * 1024 if os.name == "nt" else 64 * 1024

# Lib onfigurations.
WORKSPACE_LIB_DIR = Path(f".{APP_NAME}")
WORKSPACE_CONFIG_DIR = WORKSPACE_LIB_DIR
WORKSPACE_CONFIG_FILE = WORKSPACE_LIB_DIR / "config.json"
WORKSPACE_EXTENSIONS_VENV_DIR = WORKSPACE_LIB_DIR / "extensions"
EXTENSIONS_DIR = Path("lib") / APP_NAME
USER_REPO_CONFIG = Path("repo.json")
if os.name == "nt":
    local_appdata_env = os.getenv("LOCALAPPDATA")
    if not local_appdata_env or not Path(local_appdata_env).exists():
        local_appdata = Path.home() / "AppData" / "Loacal"
    else:
        local_appdata = Path(local_appdata_env)
    USER_LIB_DIR = local_appdata / APP_NAME
    USER_CONFIG_DIR = local_appdata / APP_NAME
else:
    USER_LIB_DIR = Path.home() / ".local" / APP_NAME
    USER_CONFIG_DIR = Path.home() / ".config" / APP_NAME
USER_CONFIG_FILE = USER_CONFIG_DIR / "config.json"
USER_EXTENSIONS_VENV_DIR = USER_LIB_DIR / "extensions"
# Override it in Windows later.
GLOBAL_LIB_DIR = Path("/usr/local/lib") / APP_NAME
GLOBAL_CONFIG_DIR = Path("/etc") / APP_NAME
GLOBAL_CONFIG_FILE = GLOBAL_CONFIG_DIR / "config.json"
GLOBAL_EXTENSIONS_VENV_DIR = GLOBAL_LIB_DIR / "extensions"
VENV_LOCK_FILENAME = "venv.lock"
DB_FILENAME = f"{APP_NAME}.db"


# Logging configurations.
# We don't need to absolute the path because rubisco supports '--root'
# option.
LOG_FILE = WORKSPACE_LIB_DIR / f"{APP_NAME}.log"
LOG_FORMAT = "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s"
LOG_REGEX = r"\[(.*)\] \[(.*)\] \[(.*)\] (.*)"
LOG_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_LEVEL = "DEBUG"
PIP_LOG_FILE = WORKSPACE_LIB_DIR / "pip.log"
DEFAULT_LOG_KEEP_LINES = 5000


# Constants that are not configurable.
STDOUT_IS_TTY = sys.stdout.isatty()
PROGRAM_PATH: Path = Path(sys.argv[0]).resolve()
if not sys.argv[0]:
    PROGRAM_PATH = Path(__file__).resolve().parent

PYTHON_PATH: Path | None = Path(sys.executable).resolve()
# If the program is running in a packed environment. (e.g. PyInstaller)
IS_PACKED = getattr(sys, "frozen", False) or hasattr(sys, "_MEIPASS")

if IS_PACKED:
    RUBISCO_COMMAND = command(str(PROGRAM_PATH))
    PYTHON_PATH = None
else:
    RUBISCO_COMMAND = command([str(PYTHON_PATH), str(PROGRAM_PATH)])

PROGRAM_DIR: Path = PROGRAM_PATH.parent.absolute()

if os.name == "nt":  # On Windows.
    GLOBAL_LIB_DIR = PROGRAM_DIR
    GLOBAL_CONFIG_DIR = PROGRAM_DIR / "config"
    GLOBAL_CONFIG_FILE = GLOBAL_CONFIG_DIR / "config.json"
    GLOBAL_EXTENSIONS_VENV_DIR = GLOBAL_LIB_DIR / "extensions"
