import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from frames.base_frame import BaseFrame


class ChartFrame(BaseFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.init_widgets()
        self.set_defaults()

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
