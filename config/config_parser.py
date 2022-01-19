"""Parse configurations from default.yml File."""

from distutils.util import strtobool
from pathlib import Path
import sys

from configargparse import ArgParser, YAMLConfigFileParser


BASE_DIR = Path(__file__).parent
YAML_FILE = "default.yaml"
DEFAULT_CONFIG_FILE = f"{BASE_DIR}/{YAML_FILE}"

parser = ArgParser(
    config_file_parser_class=YAMLConfigFileParser,
    default_config_files=[DEFAULT_CONFIG_FILE],
    auto_env_var_prefix="",
)

# Environment
parser.add("--ENV", help="ENV")

# Security related parameters
parser.add("--ZATTOO_HTTP_BEARER_TOKEN", help="ZATTOO_HTTP_BEARER_TOKEN")

# Zattoo web server parameters
parser.add("--HOST", help="HOST")
parser.add("--PORT", help="PORT")
# `strtobool` will make sure only boolean'able values are accepted.
parser.add("--DEBUG", help="DEBUG", type=lambda x: bool(strtobool(x)))
parser.add("--ZATTOO_MAIN_URL", help="ZATTOO_MAIN_URL")

# Postgresql parameters
parser.add("--POSTGRES_ZATTOO_READ_WRITE", help="POSTGRES_ZATTOO_READ_WRITE")

argument_options = parser.parse_known_args(sys.argv)
# print(parser.format_values())

current_config = argument_options[0]
