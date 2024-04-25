import tkinter
from frames.base_frame import BaseFrame
import sercom.fastprotoc as fastprotoc
from event_bus import EventBus
from config import Config
import widgets


class StatusBarFrame(BaseFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.event_bus = EventBus()
        self.m_config = Config()

        self.version = self.m_config.get_version()
        self.connection_state = tkinter.BooleanVar()
        self.connection_state_dict = {
            True: "Connected",
            False: "Disconnected"
        }

        self.grid_columnconfigure(1, weight=1)
        self.init_widgets()
        self.set_defaults()

        self.event_bus.subscribe(fastprotoc.CONNECTION_UPDATE, self.connection_state_update_callback)

    def init_widgets(self):
        self.version_hint = widgets.StatusIcon(self)
        self.version_hint.grid(row=0, column=0, padx=(10, 0), pady=(5, 5), sticky="nsew")
        
        self.connection_hint = widgets.StatusIcon(self, image_light="img/signal-light.png", image_dark="img/signal-dark.png", text="Disconnected")
        self.connection_hint.grid(row=0, column=2, padx=(10, 0), pady=(5, 5), sticky="nsew")

    def set_defaults(self):
        text = "Version {}".format(self.version)
        self.version_hint.configure(text=text)

    def connection_state_update_callback(self, data):
        self.connection_hint.configure(text=self.connection_state_dict[data])
