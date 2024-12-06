"""
This module provides functionality to load and access configuration data 
from a YAML file, specifically for database configurations.

Functions:
    - load_config(dir): Loads the configuration data from a YAML file.
    - get_config(): Retrieves the loaded configuration data.

Global Variables:
    - config_data: A dictionary holding the configuration data after being loaded.
"""
import os
import yaml

# Global variable to hold the loaded configuration data
config_data = None

def load_config(dir):
    """
    Loads the configuration data from a YAML file located in the specified directory.

    Args:
        dir (str): The base directory containing the `config` folder where the `database.yml` file resides.

    Raises:
        FileNotFoundError: If the `database.yml` file does not exist in the specified path.
        yaml.YAMLError: If there is an error parsing the YAML file.

    Example:
        >>> load_config('/path/to/project')
        Configuration data is loaded and accessible via `get_config`.
    """
    global config_data

    config_file_path = os.path.join(dir, 'config', 'database.yml')
    #print("config_file_path",config_file_path)    
    with open(config_file_path, 'r') as f:
        config_data = yaml.safe_load(f)

def get_config():
    """
    Retrieves the loaded configuration data.

    Returns:
        dict: The configuration data loaded by `load_config`.

    Raises:
        RuntimeError: If the configuration has not been loaded yet.

    Example:
        >>> load_config('/path/to/project')
        >>> config = get_config()
        >>> print(config)
    """
    #print(config_data)
    if config_data is None:
        raise RuntimeError("Configuration not loaded. Call load_config() first.")
    return config_data