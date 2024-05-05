import queue

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.interpolate import interp1d

import sercom
from sercom.fastprotoc import PacketType
from config import Config
from event_bus import EventBus, Event
from frames.base_frame import BaseFrame


class PlotFrame(BaseFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.sercom = sercom.Sercom()
        self.event_bus = EventBus()
        self.m_config = Config()

        self.after_ids = []
        self.hall_queue = queue.Queue()
        self.pwm_queue = queue.Queue()
        self.sercom.add_getter_queue(PacketType.HALL_UPDATE.value, self.hall_queue)
        self.sercom.add_getter_queue(PacketType.PWM_UPDATE.value, self.pwm_queue)

        self.padding = 25
        self.prev_padding_value = 0
        self.max_data_points = 250
        self.scroll_threshold = self.max_data_points / 50

        self.setpoint = 0
        self.x_hall_data = []
        self.y_hall_data = []
        self.y_setpoint_data = []
        self.x_pwm_data = []
        self.y_pwm_data = []

        self.master = master
        self.init_widgets()
        self.set_defaults()

        self.event_bus.subscribe(Event.SERIAL_OPENED.value, self.start_plotting)
        self.event_bus.subscribe(Event.SERIAL_CLOSED.value, self.stop_plotting)
        self.event_bus.subscribe(PacketType.SETPOINT_UPDATE.value, self.setpoint_update_callback)
        self.event_bus.subscribe("WM_DELETE_WINDOW", self.window_close_callback)

    def init_widgets(self):
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(9, 9), gridspec_kw={'height_ratios': [2, 1]}, constrained_layout=True)

        self.hall_line, = self.ax1.plot([], [], lw=2)
        self.setpoint_line, = self.ax1.plot([], [], lw=2, linestyle='--', color="red")
        self.ax1.set_xlabel('Time', fontsize=12)
        self.ax1.set_ylabel('Value', fontsize=12)
        self.ax1.tick_params(axis='both', which='major', labelsize=10)
        self.ax1.grid(True, linestyle='--', alpha=0.7)
        self.ax1.set_title('Hall-Sensor Output', fontsize=14, fontweight='bold')

        self.pwm_line, = self.ax2.plot([], [], lw=1)
        self.ax2.set_xlabel('X Label', fontsize=12)
        self.ax2.set_ylabel('Y Label', fontsize=12)
        self.ax2.tick_params(axis='both', which='major', labelsize=10)
        self.ax2.grid(True, linestyle='--', alpha=0.7)
        self.ax2.set_title('PWM Signal', fontsize=14, fontweight='bold')
        self.ax2.set_ylim(-45, 300)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().grid(row=0, column=1, padx=(50, 50), pady=(50, 50), sticky="nsew")

    def set_defaults(self):
        pass

    def window_close_callback(self, event_data=None):
        """Callback function for window close event."""
        for after_id in self.after_ids:
            self.after_cancel(after_id)

    def setpoint_update_callback(self, event_data=None):
        """Callback function for update setpoint event."""
        self.setpoint = event_data

    def start_plotting(self, event_data=None):
        self.ani = animation.FuncAnimation(self.fig, self.update_plot, interval=5, cache_frame_data=False, blit=True)

    def stop_plotting(self, event_data=None):
        for after_id in self.after_ids:
            self.after_cancel(after_id)

        self.ani.event_source.stop()

    def update_plot(self, frame):
        """Update plot from data queue."""
        while not self.hall_queue.empty():
            new_x, new_y = self.hall_queue.get()
            self.x_hall_data.append(new_x)
            self.y_hall_data.append(new_y)
            self.y_setpoint_data.append(self.setpoint)

            if len(self.x_hall_data) > self.max_data_points:
                self.x_hall_data = self.x_hall_data[-self.max_data_points:]
                self.y_hall_data = self.y_hall_data[-self.max_data_points:]
                self.y_setpoint_data = self.y_setpoint_data[-self.max_data_points:]

            if new_x > self.scroll_threshold:
                self.ax1.set_xlim(new_x - self.scroll_threshold, new_x)

        while not self.pwm_queue.empty():
            new_x, new_y = self.pwm_queue.get()
            self.x_pwm_data.append(new_x)

            prev_y = self.y_pwm_data[-1] if len(self.y_pwm_data) > 0 else None
            if prev_y is not None and (new_y > 0 and new_y < 255):
                self.y_pwm_data.append(255)
            else:
                self.y_pwm_data.append(new_y)

            if len(self.x_pwm_data) > self.max_data_points:
                self.x_pwm_data = self.x_pwm_data[-self.max_data_points:]
                self.y_pwm_data = self.y_pwm_data[-self.max_data_points:]

            if new_x > self.scroll_threshold:
                self.ax2.set_xlim(new_x - self.scroll_threshold, new_x)

        if len(self.x_hall_data) < 4:
            self.hall_line.set_data([], [])
            self.setpoint_line.set_data([], [])
        else:
            f_interp = interp1d(self.x_hall_data, self.y_hall_data, kind='cubic')
            x_interp = np.linspace(min(self.x_hall_data), max(self.x_hall_data), 1000)
            y_interp = f_interp(x_interp)

            y_range = max(y_interp) - min(y_interp)
            padding_value = y_range * self.padding / 100

            if abs(padding_value - self.prev_padding_value) >= 2:
                min_y = min(y_interp) - padding_value
                max_y = max(y_interp) + padding_value
                self.ax1.set_ylim(min_y, max_y)
                self.prev_padding_value = padding_value

            self.hall_line.set_data(x_interp, y_interp)
            self.setpoint_line.set_data(self.x_hall_data, self.y_setpoint_data)
            pwm_step = np.array(self.y_pwm_data[:-1])
            pwm_step = np.repeat(pwm_step, 5)
            pwm_step = np.insert(pwm_step, 0, pwm_step[0])
            self.x_pwm_step = np.linspace(min(self.x_pwm_data), max(self.x_pwm_data), len(pwm_step))
            self.pwm_line.set_data(self.x_pwm_step, pwm_step)

        return self.hall_line, self.setpoint_line, self.pwm_line
