import customtkinter
import queue
import tkinter
import widgets
import sercom
from sercom.fastprotoc import PacketType
from event_bus import EventBus, Event
from frames.base_frame import BaseFrame


class SettingsFrame(BaseFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.sercom = sercom.Sercom()
        self.event_bus = EventBus()

        self.realtime_enabled = tkinter.BooleanVar()
        self.setpoint_queue = queue.Queue()
        self.kp_queue = queue.Queue()
        self.ki_queue = queue.Queue()
        self.kd_queue = queue.Queue()
        self.prev_values = {
            'setpoint': None,
            'kp': None,
            'ki': None,
            'kd': None
        }

        self.grid_rowconfigure(5, weight=1)
        self.init_widgets()
        self.set_defaults()

        self.sercom.add_setter_queue(PacketType.SETPOINT_UPDATE.value, self.setpoint_queue)
        self.sercom.add_setter_queue(PacketType.KP_UPDATE.value, self.kp_queue)
        self.sercom.add_setter_queue(PacketType.KI_UPDATE.value, self.ki_queue)
        self.sercom.add_setter_queue(PacketType.KD_UPDATE.value, self.kd_queue)

        self.event_bus.subscribe(Event.SERIAL_CLOSED.value, self.set_defaults)
        self.event_bus.subscribe(PacketType.SETPOINT_UPDATE.value, lambda event_data: self.update_callback('setpoint')(event_data))
        self.event_bus.subscribe(PacketType.KP_UPDATE.value, lambda event_data: self.update_callback('kp')(event_data))
        self.event_bus.subscribe(PacketType.KI_UPDATE.value, lambda event_data: self.update_callback('ki')(event_data))
        self.event_bus.subscribe(PacketType.KD_UPDATE.value, lambda event_data: self.update_callback('kd')(event_data))

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
        self.setpoint_spinbox.set(0)
        self.kp_spinbox.set(0)
        self.ki_spinbox.set(0)
        self.kd_spinbox.set(0)

        for key in self.prev_values:
            self.prev_values[key] = self.get_current_value(key)

    def realtime_apply_callback(self):
        "Callback function for realtime checkbox click event."
        if self.realtime_enabled.get():
            self.apply_button.configure(state="disabled")
        elif self.sercom.is_connected():
            changes_detected = any(self.get_current_value(key) != self.prev_values[key] for key in self.prev_values)
            if changes_detected:
                self.apply_button.configure(state="normal")

    def update_callback(self, key):
        """Callback function for a specific key."""
        def callback(event_data=None):
            if event_data is not None:
                self.set_current_value(key, event_data)
        return callback

    def update_gui(self, key):
        """Callback function for a specific key (GUI)."""
        def callback():
            value = self.get_current_value(key)
            queue = getattr(self, f'{key}_queue')
            if self.realtime_switch.get() and queue is not None:
                queue.put(value)
            elif self.sercom.is_connected():
                self.apply_button.configure(state="normal")
        return callback

    def get_current_value(self, key):
        """Get the current value of a setting."""
        return getattr(self, f'{key}_spinbox').get()

    def set_current_value(self, key, value):
        """Set the current value of a setting."""
        getattr(self, f'{key}_spinbox').set(value)
        self.prev_values[key] = self.get_current_value(key)

    def apply_changes(self):
        """Apply the changes."""
        for key in self.prev_values:
            current_value = self.get_current_value(key)
            if current_value != self.prev_values[key]:
                queue = getattr(self, f'{key}_queue')
                if queue is not None:
                    queue.put(current_value)
                self.prev_values[key] = current_value
        self.apply_button.configure(state="disabled")

    def store(self):
        pass
