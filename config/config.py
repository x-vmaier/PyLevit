import json


class Config:
    _instance = None

    def __new__(cls):
        """Create a new instance of Config class if it doesn't exist."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config_file = "config.json"
        return cls._instance

    def _load_config(self):
        """Load configuration data from the config file."""
        try:
            with open(self.config_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print("Config file not found.")
        except json.JSONDecodeError:
            print("Invalid JSON format in config file.")
        except Exception as e:
            print(f"Error reading config file: {e}")
        return {}

    def _save_config(self, config_data):
        """Save configuration data to the config file."""
        try:
            with open(self.config_file, "w") as f:
                json.dump(config_data, f, indent=4)
        except PermissionError:
            print("Permission denied. Cannot write to config file.")
        except Exception as e:
            print(f"Error writing to config file: {e}")

    def get(self, *keys):
        """Get a specific configuration setting."""
        config_data = self._load_config()
        for key in keys:
            config_data = config_data.get(key, {})
        return config_data

    def set(self, *keys, value):
        """Set a specific configuration setting."""
        config_data = self._load_config()
        nested_dict = config_data
        for key in keys[:-1]:
            nested_dict = nested_dict.setdefault(key, {})
        nested_dict[keys[-1]] = value
        self._save_config(config_data)
