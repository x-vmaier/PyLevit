import asyncio
import tkinter
import customtkinter
from frames.base_frame import BaseFrame
from event_bus import EventBus
import sercom.fastprotoc
import widgets
import sercom.fastprotoc as fastprotoc
import sercom


class SettingsFrame(BaseFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.serial = sercom.Serial()
        self.event_bus = EventBus()

        self.realtime_enabled = tkinter.BooleanVar()
        self.prev_values = {
            'setpoint': None,
            'kp': None,
            'ki': None,
            'kd': None
        }

        self.grid_rowconfigure(5, weight=1)
        self.init_widgets()
        self.set_defaults()

        self.event_bus.subscribe(fastprotoc.SETPOINT_UPDATE, self.update_callback('setpoint'))
        self.event_bus.subscribe(fastprotoc.KP_UPDATE, self.update_callback('kp'))
        self.event_bus.subscribe(fastprotoc.KI_UPDATE, self.update_callback('ki'))
        self.event_bus.subscribe(fastprotoc.KD_UPDATE, self.update_callback('kd'))

    def init_widgets(self):
        self.frame_title = customtkinter.CTkLabel(self, text="Settings", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.frame_title.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10))

        self.setpoint_spinbox = widgets.FloatSpinbox(self, text="Setpoint:", width=130, command=self.update_gui('setpoint'))
        self.setpoint_spinbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.kp_spinbox = widgets.FloatSpinbox(self, text="Kp:", width=130, command=self.update_gui('kp'))
        self.kp_spinbox.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.ki_spinbox = widgets.FloatSpinbox(self, text="Ki:", width=130, command=self.update_gui('ki'))
        self.ki_spinbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.kd_spinbox = widgets.FloatSpinbox(self, text="Kd:",  width=130, command=self.update_gui('kd'))
        self.kd_spinbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.realtime_switch = customtkinter.CTkCheckBox(master=self, text="Apply in Realtime", variable=self.realtime_enabled, command=self.realtime_apply_callback)
        self.realtime_switch.grid(row=6, column=0, columnspan=2, padx=(0, 80), pady=(10, 0))

        self.apply_button = customtkinter.CTkButton(self, text="Apply", width=100, state="disabled", command=self.apply_changes)
        self.apply_button.grid(row=7, column=0, padx=(10, 5))

        self.save_button = customtkinter.CTkButton(self, text="Store", width=100, state="disabled", command=self.store)
        self.save_button.grid(row=7, column=1, padx=(5, 10), pady=10)

    def set_defaults(self):
        for key in self.prev_values:
            self.prev_values[key] = self.get_current_value(key)

    def update_callback(self, key):
        """Create update callback function for a specific key."""
        def callback(event=None, data=None):
            if event:
                value = self.get_current_value(key)
                if self.realtime_switch.get():
                    asyncio.run(fastprotoc.send(self.serial, getattr(fastprotoc, f'{key.upper()}_UPDATE'), value))
                else:
                    self.apply_button.configure(state="normal")
            elif data is not None:
                self.set_current_value(key, data)
        return callback

    def update_gui(self, key):
        """Create GUI update function for a specific key."""
        def callback(event=None):
            value = self.get_current_value(key)
            if self.realtime_switch.get():
                asyncio.run(fastprotoc.send(self.serial, getattr(fastprotoc, f'{key.upper()}_UPDATE'), value))
            elif self.serial.is_connected():
                self.apply_button.configure(state="normal")
        return callback

    def get_current_value(self, key):
        """Get the current value of a setting."""
        return getattr(self, f'{key}_spinbox').get()

    def set_current_value(self, key, value):
        """Set the current value of a setting."""
        getattr(self, f'{key}_spinbox').set(value)

    def realtime_apply_callback(self):
        if self.realtime_enabled.get():
            self.apply_button.configure(state="disabled")
        elif self.serial.is_connected():
            changes_detected = any(self.get_current_value(key) != self.prev_values[key] for key in self.prev_values)
            if changes_detected:
                self.apply_button.configure(state="normal")

    def apply_changes(self):
        """Apply the changes."""
        for key in self.prev_values:
            current_value = self.get_current_value(key)
            if current_value != self.prev_values[key]:
                asyncio.run(fastprotoc.send(self.serial, getattr(fastprotoc, f'{key.upper()}_UPDATE'), current_value))
                self.prev_values[key] = current_value
        self.apply_button.configure(state="disabled")

    def store(self):
        pass
