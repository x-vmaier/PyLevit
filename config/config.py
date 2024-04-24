import json

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config_file = 'config.json'
        return cls._instance

    def get_version(self):
        """Get the version from the config file."""
        try:
            with open(self.config_file, 'r') as f:
                version_info = json.load(f)
                return version_info.get('version', 'Unknown')
        except FileNotFoundError:
            print("Config file not found.")
            return 'Unknown'
        except json.JSONDecodeError:
            print("Invalid JSON format in config file.")
            return 'Unknown'
        except Exception as e:
            print(f"Error reading config file: {e}")
            return 'Unknown'

    def get_config(self, key):
        """Get a specific configuration setting."""
        try:
            with open(self.config_file, 'r') as f:
                config_data = json.load(f)
                return config_data.get(key)
        except FileNotFoundError:
            print("Config file not found.")
            return None
        except json.JSONDecodeError:
            print("Invalid JSON format in config file.")
            return None
        except Exception as e:
            print(f"Error reading config file: {e}")
            return None

    def set_config(self, key, value):
        """Set a specific configuration setting."""
        try:
            with open(self.config_file, 'r+') as f:
                config_data = json.load(f)
                config_data[key] = value
                f.seek(0)
                json.dump(config_data, f, indent=4)
                f.truncate()
        except FileNotFoundError:
            print("Config file not found.")
        except json.JSONDecodeError:
            print("Invalid JSON format in config file.")
        except Exception as e:
            print(f"Error updating config file: {e}")
