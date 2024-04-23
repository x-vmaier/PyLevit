import queue
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.interpolate import interp1d
from frames.base_frame import BaseFrame
from sercom.packet import PacketType
import sercom


class ChartFrame(BaseFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.serial = sercom.Serial.get_instance()
        self.hall_queue = queue.Queue()
        self.setpoint = queue.Queue()
        self.serial.reader.add_data_queue(PacketType.HALL_UPDATE, self.hall_queue)
        self.serial.reader.add_data_queue(PacketType.SETPOINT_UPDATE, self.setpoint)

        self.master = master
        self.init_widgets()
        self.set_defaults()

        self.after(100, self.update_chart_from_queue)

    def init_widgets(self):
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(9, 9), gridspec_kw={'height_ratios': [2, 1]}, constrained_layout=True)

        # First subplot for real-time data
        self.line, = self.ax1.plot([], [], lw=2)
        self.setpoint_line, = self.ax1.plot([], [], lw=1)
        self.ax1.set_xlabel('Time', fontsize=12)
        self.ax1.set_ylabel('Value', fontsize=12)
        self.ax1.tick_params(axis='both', which='major', labelsize=10)
        self.ax1.grid(True, linestyle='--', alpha=0.7)
        self.ax1.set_title('Hall-Sensor Output', fontsize=14, fontweight='bold')

        # Second subplot for additional data
        self.ax2.set_xlabel('X Label', fontsize=12)
        self.ax2.set_ylabel('Y Label', fontsize=12)
        self.ax2.tick_params(axis='both', which='major', labelsize=10)
        self.ax2.grid(True, linestyle='--', alpha=0.7)
        self.ax2.set_title('PWM Signal', fontsize=14, fontweight='bold')

        # Creating canvas for the figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().grid(row=0, column=1, padx=(50, 50), pady=(50, 50), sticky="nsew")

        # Initialize empty data for the chart
        self.padding = 15
        self.prev_padding_value = 0
        self.max_data_points = 200
        self.scroll_threshold = 10
        self.setpoint_data = []
        self.x_data = []
        self.y_data = []

    def set_defaults(self):
        pass

    def update_chart_from_queue(self):
        """Update chart from data queue."""
        while not self.hall_queue.empty():
            new_x, new_y = self.hall_queue.get()
            # Add new data points
            self.x_data.append(new_x)
            self.y_data.append(new_y)
            self.setpoint_data.append(float(self.setpoint.get()))

            # Truncate data if exceeding maximum number of data points
            if len(self.x_data) > self.max_data_points:
                self.x_data = self.x_data[-self.max_data_points:]
                self.y_data = self.y_data[-self.max_data_points:]
                self.setpoint_data = self.setpoint_data[-self.max_data_points:]

            # Check if horizontal scrolling is needed
            if new_x > self.scroll_threshold:
                self.ax.set_xlim(new_x - self.scroll_threshold, new_x)

        if len(self.x_data) < 4:  # Check if there's enough data for cubic spline interpolation
            # Clear the plot
            self.line.set_data([], [])
            self.setpoint_line.set_data([], [])
        else:
            # Perform cubic spline interpolation
            f_interp = interp1d(self.x_data, self.y_data, kind='cubic')

            # Generate interpolated x values for a smoother plot
            x_interp = np.linspace(min(self.x_data), max(self.x_data), 1000)

            # Compute interpolated y values
            y_interp = f_interp(x_interp)

            # Calculate padding as a percentage of the y-axis range
            y_range = max(y_interp) - min(y_interp)
            padding_value = y_range * self.padding / 100

            # Determine if autoscaling is needed
            if abs(padding_value - self.prev_padding_value) >= 1:
                # Manually set y-axis limits with padding
                min_y = min(y_interp) - padding_value
                max_y = max(y_interp) + padding_value
                self.ax.set_ylim(min_y, max_y)
                self.prev_padding_value = padding_value

            # Update the plot with interpolated data
            self.line.set_data(x_interp, y_interp)
            self.setpoint_line.set_data(self.x_data, self.setpoint_data)

        # Redraw the canvas
        self.canvas.draw()

        # Schedule the function to be called again
        self.after(100, self.update_chart_from_queue)
