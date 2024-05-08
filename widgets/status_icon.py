import customtkinter
from PIL import Image


class StatusIcon(customtkinter.CTkButton):
    """Custom status icon widget for the status bar."""
    def __init__(self, master, image_light: str = None, image_dark: str = None, *args, **kwargs):
        self.image = None

        if image_dark and image_light:
            self.image = customtkinter.CTkImage(
                light_image=Image.open(image_light),
                dark_image=Image.open(image_dark),
                size=(10, 10)
            )

        super().__init__(
            master,
            image=self.image if self.image else None,
            compound="right",
            width=18,
            height=18,
            fg_color="transparent",
            hover=False,
            text_color="gray",
            *args,
            **kwargs
        )
