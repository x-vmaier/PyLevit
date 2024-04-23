import customtkinter


class App(customtkinter.CTk):
    """Main application class."""
    def __init__(self):
        super().__init__()
        self.title("PyLevit")
        self.geometry(f"{1100}x{580}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)


if __name__ == "__main__":
    app = App()
    app.mainloop()
