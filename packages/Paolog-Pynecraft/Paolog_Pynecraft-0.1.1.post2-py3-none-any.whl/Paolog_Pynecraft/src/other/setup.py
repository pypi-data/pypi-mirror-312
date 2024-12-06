import os

from ...src.other.get_config_path import get_pynecraft_config_path as conf_path
from ...src.other.settings import create_node

def setup_pynecraft():
    os.mkdir(conf_path())
    create_node("PYNECRAFT")
    os.mkdir(conf_path() + "/worlds")
