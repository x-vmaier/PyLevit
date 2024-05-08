from enum import Enum


class Event(Enum):
    SERIAL_OPENED = 50
    SERIAL_CLOSED = 51
    LOGGER_EVENT = 52


class EventBus:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.subscribers = {}
        return cls._instance
    
    def subscribe(self, event_type, callback):
        """Subscribe to an event."""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def unsubscribe(self, event_type, callback):
        """Unsubscribe from an event."""
        if event_type in self.subscribers:
            self.subscribers[event_type].remove(callback)

    def publish(self, event_type, event_data=None):
        """Publish an event."""
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                try:
                    callback(event_data) if event_data is not None else callback()
                except Exception as e:
                    print(f"Error occurred while executing callback for {event_type}: {e}")
