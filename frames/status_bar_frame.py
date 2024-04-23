from frames.base_frame import BaseFrame
import widgets


class StatusBarFrame(BaseFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.grid_columnconfigure(1, weight=1)
        self.init_widgets()
        self.set_defaults()

    def init_widgets(self):
        self.version = widgets.StatusIcon(self, text="Verison 1.0.0")
        self.version.grid(row=0, column=0, padx=(10, 0), pady=(5, 5), sticky="nsew")
        self.connected = widgets.StatusIcon(self, image_light="img/signal-light.png", image_dark="img/signal-dark.png", text="Connected")
        self.connected.grid(row=0, column=2, padx=(10, 0), pady=(5, 5), sticky="nsew")

    def set_defaults(self):
        pass
