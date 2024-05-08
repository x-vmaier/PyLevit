import tkinter
import customtkinter
import widgets
from config import Config
from event_bus import EventBus, Event
from frames.base_frame import BaseFrame


class StatusBarFrame(BaseFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.event_bus = EventBus()
        self.m_config = Config()

        self.version = self.m_config.get("version")
        self.connection_state = tkinter.BooleanVar()

        self.grid_columnconfigure(1, weight=1)
        self.init_widgets()
        self.set_defaults()

        self.event_bus.subscribe(Event.SERIAL_OPENED.value, self.serial_opened_callback)
        self.event_bus.subscribe(Event.SERIAL_CLOSED.value, self.serial_closed_callback)
        self.event_bus.subscribe(Event.LOGGER_EVENT.value, self.logger_event_callback)

    def init_widgets(self):
        self.version_hint = widgets.StatusIcon(self)
        self.version_hint.grid(row=0, column=0, padx=(10, 0), pady=(5, 5), sticky="nsew")

        self.debug_output = customtkinter.CTkLabel(self, compound="right", width=18, height=20)
        self.debug_output.grid(row=0, column=1, padx=(20, 0), pady=(5, 5), sticky="nsw")
        
        self.connection_hint = widgets.StatusIcon(self, image_light="img/signal-light.png", image_dark="img/signal-dark.png", text="Disconnected")
        self.connection_hint.grid(row=0, column=2, padx=(10, 0), pady=(5, 5), sticky="nsew")

    def set_defaults(self):
        text = "Version {}".format(self.version)
        self.version_hint.configure(text=text)

    def serial_opened_callback(self, event_data=None):
        """Callback function for serial connect event."""
        self.connection_hint.configure(text="Connected")

    def serial_closed_callback(self, event_data=None):
        """Callback function for serial disconnect event."""
        self.connection_hint.configure(text="Disconnected")

    def logger_event_callback(self, event_data):
        """Callback function for updating the debug output label"""
        text, color = event_data
        self.debug_output.configure(text=text, fg=color)
