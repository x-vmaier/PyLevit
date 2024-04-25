import queue
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.interpolate import interp1d
from frames.base_frame import BaseFrame
from event_bus import EventBus
import sercom.fastprotoc as fastprotoc
from config import Config
import sercom


class ChartFrame(BaseFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.serial = sercom.Serial()
        self.event_bus = EventBus()
        self.config = Config()

        self.after_ids = []
        self.hall_queue = queue.Queue()
        self.pwm_queue = queue.Queue()
        self.serial.add_data_queue(fastprotoc.HALL_UPDATE, self.hall_queue)
        self.serial.add_data_queue(fastprotoc.PWM_UPDATE, self.pwm_queue)

        self.padding = 15
        self.prev_padding_value = 0
        self.max_data_points = 200
        self.scroll_threshold = 10
        self.setpoint = 0
        self.x_data = []
        self.y_setpoint_data = []
        self.y_hall_data = []
        self.y_pwm_data = []

        self.master = master
        self.init_widgets()
        self.set_defaults()

        self.event_bus.subscribe(fastprotoc.SETPOINT_UPDATE, self.setpoint_update_callback)
        self.event_bus.subscribe("WM_DELETE_WINDOW", self.window_close_callback)
        self.after_ids.append(self.after(100, self.update_chart_from_queue))

    def init_widgets(self):
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(9, 9), gridspec_kw={'height_ratios': [2, 1]}, constrained_layout=True)

        self.hall_line, = self.ax1.plot([], [], lw=2)
        self.setpoint_line, = self.ax1.plot([], [], lw=2, linestyle='--', color="red")
        self.ax1.set_xlabel('Time', fontsize=12)
        self.ax1.set_ylabel('Value', fontsize=12)
        self.ax1.tick_params(axis='both', which='major', labelsize=10)
        self.ax1.grid(True, linestyle='--', alpha=0.7)
        self.ax1.set_title('Hall-Sensor Output', fontsize=14, fontweight='bold')

        self.pwm_line, = self.ax2.plot([], [], lw=2)
        self.ax2.set_xlabel('X Label', fontsize=12)
        self.ax2.set_ylabel('Y Label', fontsize=12)
        self.ax2.tick_params(axis='both', which='major', labelsize=10)
        self.ax2.grid(True, linestyle='--', alpha=0.7)
        self.ax2.set_title('PWM Signal', fontsize=14, fontweight='bold')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().grid(row=0, column=1, padx=(50, 50), pady=(50, 50), sticky="nsew")

    def set_defaults(self):
        pass

    def window_close_callback(self):
        for after_id in self.after_ids:
            self.after_cancel(after_id)

    def setpoint_update_callback(self, data):
        self.setpoint = data

    def update_chart_from_queue(self):
        """Update chart from data queue."""
        while not self.hall_queue.empty():
            new_x, new_y = self.hall_queue.get()

            self.x_data.append(new_x)
            self.y_hall_data.append(new_y)
            self.y_setpoint_data.append(self.setpoint)

            if len(self.x_data) > self.max_data_points:
                self.x_data = self.x_data[-self.max_data_points:]
                self.y_hall_data = self.y_hall_data[-self.max_data_points:]
                self.y_setpoint_data = self.y_setpoint_data[-self.max_data_points:]

            if new_x > self.scroll_threshold:
                self.ax1.set_xlim(new_x - self.scroll_threshold, new_x)

        while not self.pwm_queue.empty():
            new_x, new_y = self.pwm_queue.get()

            self.x_data.append(new_x)
            self.y_pwm_data.append(new_y)

            if len(self.x_data) > self.max_data_points:
                self.x_data = self.x_data[-self.max_data_points:]
                self.y_pwm_data = self.y_pwm_data[-self.max_data_points:]

            if new_x > self.scroll_threshold:
                self.ax1.set_xlim(new_x - self.scroll_threshold, new_x)

        if len(self.x_data) < 4:  # Check if there's enough data for cubic spline interpolation
            self.hall_line.set_data([], [])
            self.setpoint_line.set_data([], [])
        else:
            f_interp = interp1d(self.x_data, self.y_hall_data, kind='cubic')
            x_interp = np.linspace(min(self.x_data), max(self.x_data), 1000)
            y_interp = f_interp(x_interp)

            y_range = max(y_interp) - min(y_interp)
            padding_value = y_range * self.padding / 100

            if abs(padding_value - self.prev_padding_value) >= 1:
                min_y = min(y_interp) - padding_value
                max_y = max(y_interp) + padding_value
                self.ax1.set_ylim(min_y, max_y)
                self.prev_padding_value = padding_value

            self.hall_line.set_data(x_interp, y_interp)
            self.setpoint_line.set_data(self.x_data, self.y_setpoint_data)
            self.pwm_line.set_data(self.x_data, self.y_pwm_data)

        self.canvas.draw()
        self.after(100, self.update_chart_from_queue)
