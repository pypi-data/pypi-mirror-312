from ...src.other.get_config_path import get_pynecraft_config_path as config_path

import os.path
import configparser

# What is all that?
# A settings hive is a file, like PYNECRAFT.ini
# A settings node is a node, like [USER]
# A settings key is a key, like USERNAME = ...

# Node
def create_node(settings_node_name:str):
    if (node_exists(settings_node_name)):
        # Node exists, do nothing
        pass
    else:
        with open(f"{config_path()}/{settings_node_name}.ini", "w+") as file:
            file.close()

def node_exists(settings_node_name:str) -> bool:
    return os.path.isfile(f"{config_path()}/{settings_node_name}.ini")

def delete_node(settings_node_name:str):
    if (node_exists(settings_node_name)):
        # Node exists, delete it
        os.remove(f"{config_path()}/{settings_node_name}.ini")
    else:
        # Node doesn't exists, do nothing
        print("SETTINGS_API: No need to delete file")

# Hive (Section in the INI file)
def create_hive(settings_node_name: str, settings_hive_name: str):
    config = configparser.ConfigParser()
    config_path_with_name = f"{config_path()}/{settings_node_name}.ini"
    
    if node_exists(settings_node_name):
        config.read(config_path_with_name)
        
        if not config.has_section(settings_hive_name):
            config.add_section(settings_hive_name)
            with open(config_path_with_name, "w") as configfile:
                config.write(configfile)
    else:
        print(f"SETTINGS_API: Node '{settings_node_name}' doesn't exist. Cannot create hive.")

def hive_exists(settings_node_name: str, settings_hive_name: str) -> bool:
    config = configparser.ConfigParser()
    if node_exists(settings_node_name):
        config.read(f"{config_path()}/{settings_node_name}.ini")
        return config.has_section(settings_hive_name)
    return False

def delete_hive(settings_node_name: str, settings_hive_name: str):
    config = configparser.ConfigParser()
    config_path_with_name = f"{config_path()}/{settings_node_name}.ini"
    
    if node_exists(settings_node_name):
        config.read(config_path_with_name)
        if config.has_section(settings_hive_name):
            config.remove_section(settings_hive_name)
            with open(config_path_with_name, "w") as configfile:
                config.write(configfile)
        else:
            print(f"SETTINGS_API: Hive '{settings_hive_name}' doesn't exist.")
    else:
        print(f"SETTINGS_API: Node '{settings_node_name}' doesn't exist. Cannot delete hive.")


# Key (Key-Value pair within a section/hive)
def set_key_value(settings_node_name: str, settings_hive_name: str, settings_key_name: str, value: str):
    config = configparser.ConfigParser()
    config_path_with_name = f"{config_path()}/{settings_node_name}.ini"
    
    if node_exists(settings_node_name):
        config.read(config_path_with_name)
        
        if not config.has_section(settings_hive_name):
            config.add_section(settings_hive_name)
        
        config.set(settings_hive_name, settings_key_name, value)
        
        with open(config_path_with_name, "w") as configfile:
            config.write(configfile)
    else:
        print(f"SETTINGS_API: Node '{settings_node_name}' doesn't exist. Cannot set key.")

def key_exists(settings_node_name: str, settings_hive_name: str, settings_key_name: str) -> bool:
    config = configparser.ConfigParser()
    if node_exists(settings_node_name):
        config.read(f"{config_path()}/{settings_node_name}.ini")
        return config.has_option(settings_hive_name, settings_key_name)
    return False

def delete_key(settings_node_name: str, settings_hive_name: str, settings_key_name: str):
    config = configparser.ConfigParser()
    config_path_with_name = f"{config_path()}/{settings_node_name}.ini"
    
    if node_exists(settings_node_name):
        config.read(config_path_with_name)
        
        if config.has_option(settings_hive_name, settings_key_name):
            config.remove_option(settings_hive_name, settings_key_name)
            with open(config_path_with_name, "w") as configfile:
                config.write(configfile)
        else:
            print(f"SETTINGS_API: Key '{settings_key_name}' doesn't exist.")
    else:
        print(f"SETTINGS_API: Node '{settings_node_name}' doesn't exist. Cannot delete key.")

def get_key_value(settings_node_name: str, settings_hive_name: str, settings_key_name: str) -> str:
    config = configparser.ConfigParser()
    config_path_with_name = f"{config_path()}/{settings_node_name}.ini"
    
    if node_exists(settings_node_name):
        config.read(config_path_with_name)
        
        if config.has_section(settings_hive_name):
            if config.has_option(settings_hive_name, settings_key_name):
                return config.get(settings_hive_name, settings_key_name)
            else:
                print(f"SETTINGS_API: Key '{settings_key_name}' doesn't exist.")
                return None
        else:
            print(f"SETTINGS_API: Hive '{settings_hive_name}' doesn't exist.")
            return None
    else:
        print(f"SETTINGS_API: Node '{settings_node_name}' doesn't exist.")
        return None
