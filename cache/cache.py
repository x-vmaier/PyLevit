import pickle
import os
import threading


class PersistentCache:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.cache_file = "cache.pkl"
        return cls._instance

    @classmethod
    def _get_cache_file_path(cls):
        cache_dir = os.path.join(os.getcwd(), "tmp")
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        return os.path.join(cache_dir, cls._instance.cache_file)

    def get(self, key):
        """Get a specific cache entry."""
        try:
            cache_data = {}
            cache_file_path = self._get_cache_file_path()
            if os.path.exists(cache_file_path):
                with open(cache_file_path, "rb") as f:
                    cache_data = pickle.load(f)
            return cache_data.get(key)
        except FileNotFoundError:
            print("Cache file not found.")
            return None
        except (pickle.UnpicklingError, EOFError):
            print("Invalid pickle format in Cache file.")
            return None
        except Exception as e:
            print(f"Error reading Cache file: {e}")
            return None

    def set(self, key, value):
        """Set a specific cache entry."""
        try:
            with self._lock:
                cache_data = {}
                cache_file_path = self._get_cache_file_path()
                if os.path.exists(cache_file_path):
                    with open(cache_file_path, "rb") as f:
                        cache_data = pickle.load(f)
                cache_data[key] = value
                with open(cache_file_path, "wb") as f:
                    pickle.dump(cache_data, f)
        except Exception as e:
            print(f"Error updating Cache file: {e}")
