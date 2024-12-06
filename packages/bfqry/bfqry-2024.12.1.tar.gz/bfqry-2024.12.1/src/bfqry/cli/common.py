from pathlib import Path
from bfqry.__about__ import __version__
global logger

PROG_NAME = "bfqry"
PROG_VERSION = __version__
PROG_DESCRIPTION = "Batfish Query Utility"

SEPARATOR1 = "=" * 60
SEPARATOR2 = "-" * 50
SEPARATOR3 = "-" * 40

DEFAULT_SETTINGS = [str(Path.home()) + "/.settings.ini", str(Path.home()) + "/.config/bfqry/settings.ini","settings.ini"]
DEFAULT_HOST = "127.0.0.1"
DEFAULT_BASE = "./"
DEFAULT_PORT1 = 9997
DEFAULT_PORT2 = 9996
DEFAULT_TIMEOUT = 5.0
DEFAULT_HTTPS = False
DEFAULT_INSECURE = True
DEFAULT_NOCACHE = False

HASH_DIRS = ["configs", "hosts"]
HASH_FILES = ["interface_blacklist", "runtime_data.json", "layer1_topology.json"]
HASH_IGNORES = [".DS_Store"]
