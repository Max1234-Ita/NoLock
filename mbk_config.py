import configparser
import sys
from configparser import ConfigParser

from pathlib import Path


class MBKConfig:
    def __init__(self):
        self._config = ConfigParser()
        mypath = Path(sys.argv[0]).parent
        configfile = Path(mypath / 'config.ini')
        self._config.read(configfile)

    def get_option(self, section, option_name):
        try:
            return self._config.get(section, option_name)
            z = 0
           
        except configparser.NoSectionError:
            print(f"ERROR - Section '{section}' not found. Please check your config file.")
            
        except configparser.NoOptionError:
            print(f"ERROR - Option '{option_name}' not found in section '{section}'. Please check your config file.")
    
    def set_option(self, section, option_name, option_value):
        pass
