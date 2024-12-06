import os
import yaml
from .git import GitInfo
from tian_core import singleton

class ConfigBase(object):
    pass

@singleton
class ConfigManager:
    _path = os.path.join(os.path.dirname(__file__), 'config.yaml')

    def __init__(self, path: str = None):
        self._config = {}
        if path:
            self._path = path
        self.load_from_yaml()
        self.set()

    def get(self, key, default=None): #TODO
        """Get a value from the configuration."""
        keys = key.split('.')
        value = self._config
        for k in keys:
            value = value.get(k, default)
            if value == default:
                break
        return value

    def set(self): #TODO
        """Set environment variables from the configuration."""
        for key, value in self._config.items():
            if isinstance(value, dict):
                # Flatten the dictionary for nested keys
                for sub_key, sub_value in value.items():
                    env_var_name = f"{key.upper()}_{sub_key.upper()}"
                    if env_var_name not in os.environ:
                        os.environ[env_var_name] = str(sub_value)
            else:
                env_var_name = key.upper()
                if env_var_name not in os.environ:
                    os.environ[env_var_name] = str(value)



    def load_from_yaml(self):
        """Load the configuration from the YAML file."""
        if not os.path.isfile(self._path):
            raise FileNotFoundError(f"Configuration file '{self._path}' not found.")

        try:
            with open(self._path, 'r') as file:
                self._config = yaml.load(file, Loader=yaml.FullLoader)
        except yaml.YAMLError as e:
            raise RuntimeError(f"Error loading YAML configuration: {e}")
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred: {e}")


    def print_version():
        GitInfo().print_all() #TODO: debug only\
