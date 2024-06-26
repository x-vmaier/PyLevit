import customtkinter


class BaseFrame(customtkinter.CTkFrame):
    """Frame interface."""
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

    def init_widgets(self):
        raise NotImplementedError("Subclasses must implement init_widgets method")
    
    def set_defaults(self):
        raise NotImplementedError("Subclasses must implement set_defaults method")
