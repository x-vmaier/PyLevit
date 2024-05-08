from enum import Enum, auto
from event_bus import EventBus, Event


class LogLevel(Enum):
    INFO = auto()
    WARNING = auto()
    ERROR = auto()


class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.event_bus = EventBus()
            cls._instance.DEBUG_COLORS = {
                LogLevel.INFO: "green",
                LogLevel.WARNING: "yellow",
                LogLevel.ERROR: "red"
            }
        return cls._instance
    
    def log(self, message, log_level):
        color = self.DEBUG_COLORS.get(log_level)
        self.event_bus.publish(Event.LOGGER_EVENT, (message, color))
