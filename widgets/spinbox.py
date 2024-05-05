import customtkinter
from typing import Callable, Union
from frames.base_frame import BaseFrame


class FloatSpinbox(BaseFrame):
    """Custom spinbox widget for floating-point numbers."""
    def __init__(self, *args,
                 text: str = "",
                 width: int = 100,
                 height: int = 32,
                 step_size: Union[int, float] = 1,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.text = text
        self.width = width
        self.height = height
        self.step_size = step_size
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))
        self.grid_columnconfigure((0, 2), weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.continuous_action = False

        self.init_widgets()
        self.set_defaults()
        self.bind_events()

    def init_widgets(self):
        """Create spinbox widgets."""
        if self.text:
            padx_text = self.width // len(self.text)
            self.text_label = customtkinter.CTkLabel(self, text=self.text)
            self.text_label.grid(row=0, column=0, padx=(15, padx_text), pady=3)

        self.subtract_button = customtkinter.CTkButton(self, text="-", width=self.height-6, height=self.height-6, command=self.stop_continuous_action)
        self.entry = customtkinter.CTkEntry(self, width=self.width-(2*self.height), height=self.height-6, border_width=0)
        self.add_button = customtkinter.CTkButton(self, text="+", width=self.height-6, height=self.height-6, command=self.stop_continuous_action)

        self.subtract_button.grid(row=0, column=1, padx=3, pady=3)
        self.entry.grid(row=0, column=2, padx=3, pady=3, sticky="ew")
        self.add_button.grid(row=0, column=3, padx=3, pady=3)

    def set_defaults(self):
        """Set default value for entry."""
        self.entry.insert(0, "0.0")

    def bind_events(self):
        """Bind events to buttons."""
        self.subtract_button.bind("<ButtonPress-1>", lambda event: self.start_continuous_action(self.subtract_button_callback))
        self.subtract_button.bind("<ButtonRelease-1>", self.stop_continuous_action)
        self.add_button.bind("<ButtonPress-1>", lambda event: self.start_continuous_action(self.add_button_callback))
        self.add_button.bind("<ButtonRelease-1>", self.stop_continuous_action)
        self.entry.bind("<Return>", self.return_pressed_callback)

    def start_continuous_action(self, callback):
        """Start continuous action."""
        self.continuous_action = True
        self.after(150, callback)

    def stop_continuous_action(self, event = None):
        """Stop continuous action."""
        self.continuous_action = False

    def subtract_button_callback(self):
        """Callback function for subtract button click event."""
        try:
            value = float(self.entry.get()) - self.step_size
            self.update_value(value)
            if self.continuous_action:
                self.after(50, self.subtract_button_callback)
        except ValueError:
            pass

    def add_button_callback(self):
        """Callback function for add button click event."""
        try:
            value = float(self.entry.get()) + self.step_size
            self.update_value(value)
            if self.continuous_action:
                self.after(50, self.add_button_callback)
        except ValueError:
            pass

    def return_pressed_callback(self, event):
        """Callback function for Return key press event."""
        try:
            value = float(self.entry.get())
            self.update_value(value)
        except ValueError:
            pass

    def update_value(self, value):
        """Update value in entry."""
        self.entry.delete(0, "end")
        self.entry.insert(0, value)
        if self.command:
            self.command()

    def get(self) -> Union[float, None]:
        """Get the current value."""
        try:
            return float(self.entry.get())
        except ValueError:
            return None

    def set(self, value: float):
        """Set the value."""
        self.entry.delete(0, "end")
        self.entry.insert(0, str(float(value)))
