import customtkinter
import frames

WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 580

class App(customtkinter.CTk):
    """Main application class."""
    def __init__(self):
        super().__init__()
        self.initialize_interface()

    def initialize_interface(self):
        self.title("PyLevit")
        self.center_window(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.configure_layout()
        self.create_frames()

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width)
        y = (screen_height - height)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def configure_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

    def create_frames(self):
        self.sidebar_frame = frames.Sidebar(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

if __name__ == "__main__":
    app = App()
    app.mainloop()
