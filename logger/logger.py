from enum import Enum, auto
from frames.status_bar_frame import StatusBarFrame


class LogLevel(Enum):
    INFO = auto()
    WARNING = auto()
    ERROR = auto()


class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.DEBUG_COLORS = {
                LogLevel.INFO: "green",
                LogLevel.WARNING: "yellow",
                LogLevel.ERROR: "red"
            }
        return cls._instance
    
    def log(self, message, log_level):
        StatusBarFrame().set_debug_label(message, self.DEBUG_COLORS.get(log_level))