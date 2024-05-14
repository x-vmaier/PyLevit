import asyncio
import customtkinter
import frames
from config import Config
from event_bus import EventBus
from logger import Logger, FileSink, ConsoleSink, LogLevel
import sercom
import version as v

TITLE = "PyLevit"
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 580


class App(customtkinter.CTk):
    """Main application class."""
    def __init__(self):
        super().__init__()
        self.sercom = sercom.Sercom()
        self.event_bus = EventBus()
        self.m_config = Config()
        self.logger = Logger()

        self.m_config.set("version", value=f"{v.MAJOR}.{v.MINOR}.{v.PATCH}")
        self.initialize_interface()
        self.logger.log(LogLevel.INFO, "Successfully started PyLevit")

    def initialize_interface(self):
        self.title(TITLE)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.initialize_logger()
        self.center_window(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.configure_layout()
        self.create_frames()

    def initialize_logger(self):
        console_sink = ConsoleSink()
        self.logger.add_sink(console_sink)

        file_sink = FileSink()
        self.logger.add_sink(file_sink)

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def configure_layout(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, uniform=True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=0)

    def create_frames(self):
        self.sidebar_frame = frames.SidebarFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=3, sticky="nsew")
        self.plot_frame = frames.PlotFrame(self, fg_color="white")
        self.plot_frame.grid(row=0, column=1, padx=(10, 5), pady=(10, 5), sticky="nsew")
        self.settings_frame = frames.SettingsFrame(self)
        self.settings_frame.grid(row=0, column=2, rowspan=2, padx=(5, 10), pady=(10, 5), sticky="nsew")
        self.status_frame = frames.StatusBarFrame(self)
        self.status_frame.grid(row=2, column=1, columnspan=2, padx=10, pady=(5, 10), sticky="nsew")

    def on_close(self):
        asyncio.run(self.sercom.disconnect())
        self.event_bus.publish("WM_DELETE_WINDOW")
        self.after(1200, self.destroy())


if __name__ == "__main__":
    app = App()
    app.mainloop()
