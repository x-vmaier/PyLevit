import customtkinter


class App(customtkinter.CTk):
    """Main application class."""
    def __init__(self):
        super().__init__()
        self.title("PyLevit")
        self.geometry(f"{1100}x{580}")


if __name__ == "__main__":
    app = App()
    app.mainloop()