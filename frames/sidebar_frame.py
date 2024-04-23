import customtkinter
from frames.base_frame import BaseFrame


class SidebarFrame(BaseFrame):
    """Sidebar class representing the sidebar menu."""
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.appearance_modes = ["Light", "Dark", "System"]
        self.ui_scalings = ["80%", "90%", "100%", "110%", "120%"]
        self.available_ports = ["COM3"]

        self.grid_rowconfigure(5, weight=1)
        self.init_widgets()
        self.set_defaults()

    def init_widgets(self):
        self.logo_label = customtkinter.CTkLabel(self, text="Levitator", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.serial_label = customtkinter.CTkLabel(self, text="Select Serial Port:", anchor="w")
        self.serial_label.grid(row=1, column=0, padx=20, pady=(25, 10))
        self.serial_option_menu = customtkinter.CTkOptionMenu(self, dynamic_resizing=False, values=self.available_ports, command=self.on_serial_option_menu_click)
        self.serial_option_menu.grid(row=2, column=0, padx=20, pady=(0, 10))
        self.baud_option_menu = customtkinter.CTkOptionMenu(self, dynamic_resizing=False, values=["115200", "9600"])
        self.baud_option_menu.grid(row=3, column=0, padx=20, pady=(0, 10))
        self.connect_button = customtkinter.CTkButton(self, text="Connect", command=self.connect_to_port)
        self.connect_button.grid(row=4, column=0, padx=20, pady=(30, 0))
        self.appearance_mode_label = customtkinter.CTkLabel(self, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self, values=self.appearance_modes, command=self.on_appearance_mode_change)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self, values= self.ui_scalings, command=self.on_scaling_change)
        self.scaling_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 20))

    def set_defaults(self):
        self.appearance_mode_optionemenu.set("Light")
        self.scaling_optionemenu.set("100%")

    def on_appearance_mode_change(self, new_appearance_mode: str):
        """Change appearance mode event handler."""
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_scaling_change(self, new_scaling: str):
        """Change scaling event handler."""
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def on_serial_option_menu_click(self, event):
        """Change text to connect or disconnect based on the serial connection"""
        pass

    def connect_to_port(self):
        """Connect to serial port."""
        pass
