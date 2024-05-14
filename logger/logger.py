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
                LogLevel.WARNING: "orange",
                LogLevel.ERROR: "red"
            }
            cls._instance.sinks = []
        return cls._instance

    def add_sink(self, sink):
        self.sinks.append(sink)

    def log(self, log_level, message):
        color = self.DEBUG_COLORS.get(log_level)
        for sink in self.sinks:
            sink.process(message, color)
        self.event_bus.publish(Event.LOGGER_EVENT.value, (message, color))

    def rollback(self):
        for sink in self.sinks:
            sink.rollback()
