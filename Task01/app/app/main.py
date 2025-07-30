import tkinter as tk
from app.pages.home import Home
from app.pages.imageSelect import ImageSelect
from app.pages.scaleSelection import ScaleSelection
from app.pages.crop import CropImage
from app.pages.result import Result
from app.pages.seedSelection import SelectSeed


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Coating Thickness App")
        self.geometry("1000x600")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.image_path = None
        self.cropped_image = None
        self.scale = None 
        self.frames = {}

        for F in (Home, ImageSelect, ScaleSelection, CropImage, SelectSeed, Result):
            page = F(parent=self, controller=self)
            self.frames[F] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Home)

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()