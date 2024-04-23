import tkinter
import customtkinter
from frames.base_frame import BaseFrame
from event_bus import EventBus
import widgets
import sercom


class SettingsFrame(BaseFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.serial = sercom.Serial.get_instance()
        self.event_bus = EventBus()

        self.realtime_enabled = tkinter.BooleanVar()

        self.grid_rowconfigure(5, weight=1)
        self.init_widgets()
        self.set_defaults()

    def init_widgets(self):
        self.frame_title = customtkinter.CTkLabel(self, text="Settings", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.frame_title.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10))
        self.setpoint_spinbox = widgets.FloatSpinbox(self, text="Setpoint:", width=130, command=self.on_setpoint_change)
        self.setpoint_spinbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.kp_spinbox = widgets.FloatSpinbox(self, text="Kp:", width=130, command=self.on_kp_change)
        self.kp_spinbox.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.ki_spinbox = widgets.FloatSpinbox(self, text="Ki:", width=130, command=self.on_ki_change)
        self.ki_spinbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        self.kd_spinbox = widgets.FloatSpinbox(self, text="Kd:",  width=130, command=self.on_kd_change)
        self.kd_spinbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.realtime_switch = customtkinter.CTkCheckBox(master=self, text=f"Apply in Realtime", variable=self.realtime_enabled, command=self.realtime_apply_callback)
        self.realtime_switch.grid(row=6, column=0, columnspan=2, padx=(0, 80), pady=(10, 0))
        self.apply_button = customtkinter.CTkButton(self, text="Apply", width=100, command=self.apply)
        self.apply_button.grid(row=7, column=0, padx=(10, 5))
        self.save_button = customtkinter.CTkButton(self, text="Save", width=100, command=self.save)
        self.save_button.grid(row=7, column=1, padx=(5, 10), pady=10)

    def set_defaults(self):
        pass

    def on_setpoint_change(self, event = None):
        """Event handler to update setpoint when user hits enter."""
        setpoint = self.setpoint_spinbox.get()

    def on_kp_change(self, event = None):
        """Event handler to update KP value in GUI."""
        kp = self.kp_spinbox.get()

    def on_ki_change(self, event = None):
        """Event handler to update KI value in GUI."""
        ki = self.ki_spinbox.get()

    def on_kd_change(self, event = None):
        """Event handler to update KD value in GUI."""
        kd = self.kd_spinbox.get()

    def realtime_apply_callback(self):
        if self.realtime_enabled.get():
            self.apply_button.configure(state="disabled")
        else:
            self.apply_button.configure(state="normal")

    def apply(self):
        pass

    def save(self):
        pass
