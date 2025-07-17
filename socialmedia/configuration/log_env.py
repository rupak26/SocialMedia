import yaml
import urllib.parse
from pathlib import Path

##############################
ENVIRONMENT = "development"
#ENVIRONMENT = "production"
##############################

BASE_DIR = Path(__file__).resolve().parent

def load_config(file_path , environment = None):
    try:
        with open(file_path,"r") as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing the YAML configuration file: {e}")
    
    if environment not in config:
        raise ValueError(f"Environment '{environment}' not found in the config file.")
    
    return config[environment]


CONFIG = load_config(BASE_DIR / "config.yaml", ENVIRONMENT)

LOG_DIRECTORY = CONFIG["LOG"]["DIRECTORY"]
LOG_NAME = CONFIG["LOG"]["NAME"]
LOG_SIZE = CONFIG["LOG"]["SIZE"]


