import asyncio
import customtkinter
import sercom
from config import Config
from cache import PersistentCache
from event_bus import EventBus, Event
from frames.base_frame import BaseFrame


class SidebarFrame(BaseFrame):
    """Sidebar class representing the sidebar menu."""
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.sercom = sercom.Sercom()
        self.event_bus = EventBus()
        self.cache = PersistentCache()
        self.m_config = Config()

        self.after_ids = []
        self.available_ports = ["None"]
        self.baudrates = ["115200", "9600"]
        self.appearance_modes = ["Light", "Dark", "System"]
        self.ui_scalings = ["80%", "90%", "100%", "110%", "120%"]

        self.grid_rowconfigure(5, weight=1)
        self.init_widgets()
        self.set_defaults()
        self.get_available_ports()

        self.event_bus.subscribe(Event.SERIAL_OPENED.value, self.serial_opened_callback)
        self.event_bus.subscribe(Event.SERIAL_CLOSED.value, self.serial_closed_callback)
        self.event_bus.subscribe("WM_DELETE_WINDOW", self.window_close_callback)

    def init_widgets(self):
        self.logo_label = customtkinter.CTkLabel(self, text="Levitator", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.serial_label = customtkinter.CTkLabel(self, text="Select Serial Port:", anchor="w")
        self.serial_label.grid(row=1, column=0, padx=20, pady=(25, 10))

        self.serial_option_menu = customtkinter.CTkOptionMenu(self, dynamic_resizing=False, values=self.available_ports, command=self.serial_option_menu_callback)
        self.serial_option_menu.grid(row=2, column=0, padx=20, pady=(0, 10))

        self.baud_option_menu = customtkinter.CTkOptionMenu(self, dynamic_resizing=False, values=self.baudrates)
        self.baud_option_menu.grid(row=3, column=0, padx=20, pady=(0, 10))

        self.connect_button = customtkinter.CTkButton(self, text="Connect", command=self.connect_to_port)
        self.connect_button.grid(row=4, column=0, padx=20, pady=(30, 0))

        self.appearance_mode_label = customtkinter.CTkLabel(self, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self, values=self.appearance_modes, command=self.appearance_mode_callback)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))

        self.scaling_label = customtkinter.CTkLabel(self, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=8, column=0, padx=20, pady=(10, 0))

        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self, values=self.ui_scalings, command=self.scaling_callback)
        self.scaling_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 20))

    def set_defaults(self):
        appearance_mode = self.m_config.get("appearance_mode")
        scaling = self.m_config.get("scaling")
        scaling_float = int(scaling.replace("%", "")) / 100
        prev_com = self.cache.get('prev_com')

        self.appearance_mode_optionemenu.set(appearance_mode)
        self.scaling_optionemenu.set(scaling)

        if prev_com is not None:
            self.serial_option_menu.set(prev_com)

        customtkinter.set_appearance_mode(appearance_mode)
        customtkinter.set_widget_scaling(scaling_float)

    def window_close_callback(self):
        """Callback function for window close event."""
        for after_id in self.after_ids:
            self.after_cancel(after_id)

    def appearance_mode_callback(self, new_appearance_mode: str):
        """Callback function for appearance mode change event."""
        customtkinter.set_appearance_mode(new_appearance_mode)
        self.m_config.set("appearance_mode", new_appearance_mode)

    def scaling_callback(self, new_scaling: str):
        """Callback function for scaling change event."""
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
        self.m_config.set("scaling", new_scaling)

    def serial_option_menu_callback(self, port):
        """Callback function for serial port select event."""
        connect_button_text = "Disconnect" if port == self.sercom.get_port() else "Connect"
        baud_option_menu_state = "disabled" if port == self.sercom.get_port() else "normal"

        self.connect_button.configure(text=connect_button_text)
        self.baud_option_menu.configure(state=baud_option_menu_state)

    def serial_opened_callback(self, event_data=None):
        """Callback function for serial connect event."""
        self.baud_option_menu.configure(state="disabled")
        self.connect_button.configure(text="Disconnect")

    def serial_closed_callback(self, event_data=None):
        """Callback function for serial disconnect event."""
        self.connect_button.configure(text="Connect")
        self.baud_option_menu.configure(state="normal")

    def get_available_ports(self):
        """Get available serial ports."""
        self.update_available_ports()
        self.after_ids.append(self.after(1000, self.get_available_ports))

    def update_available_ports(self):
        """Update available serial ports."""
        prev = self.available_ports
        self.available_ports = sercom.get_available_ports()

        new_state = "disabled" if self.available_ports[0] == "None" else "normal"
        self.serial_option_menu.configure(state=new_state)
        self.baud_option_menu.configure(state=new_state)
        self.connect_button.configure(state=new_state)

        if self.available_ports != prev:
            self.serial_option_menu.configure(values=self.available_ports)

        if self.serial_option_menu.get() not in self.available_ports:
            asyncio.run(self.sercom.disconnect())
            self.serial_option_menu.set(self.available_ports[0])

    def connect_to_port(self):
        """Connect to serial port."""
        port = self.serial_option_menu.get()
        baud = self.baud_option_menu.get()
        if port == "None":
            return

        if self.connect_button.cget("text") == "Connect":
            try:
                self.cache.set('prev_com', port)
                asyncio.run(self.sercom.connect(port, baud))
            except Exception as e:
                print(f"Failed to connect: {e}")
        elif self.connect_button.cget("text") == "Disconnect":
            asyncio.run(self.sercom.disconnect())
