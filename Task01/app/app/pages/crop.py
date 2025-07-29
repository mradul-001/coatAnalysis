import tkinter as tk
from PIL import Image, ImageTk
from app.pages.result import Result
import matplotlib.pyplot as plt


class CropImage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        self.rect = None
        self.start_x = self.start_y = 0
        self.canvas_img = None

        tk.Label(
            self, text="Crop the Desired Region", font=("Avenis", 18), bg="#f0f0f0"
        ).pack(pady=10)

        self.canvas = tk.Canvas(self, bg="#ddd", cursor="cross")
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)

        self.status = tk.Label(self, text="", bg="#f0f0f0")
        self.status.pack()

        self.button_frame = tk.Frame(self, bg="#f0f0f0")
        self.button_frame.pack(pady=10)
        self.crop_btn = tk.Button(
            self.button_frame,
            text="Crop Image",
            font=("Avenis", 16),
            command=self.save_crop,
            state="disabled",
        )
        self.crop_btn.pack(side="left", padx=10)
        self.proceed_btn = tk.Button(
            self.button_frame,
            text="Process Results",
            font=("Avenis", 16),
            command=self.proceed,
            state="disabled",
        )
        self.proceed_btn.pack(side="left", padx=10)

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        if hasattr(self.controller, "image_path") and self.controller.image_path:
            self.load_image(self.controller.image_path)

    def load_image(self, image_path):
        if not hasattr(self, "clicks"):
            self.clicks = []
        else:
            self.clicks.clear()
        self.status.config(text="")
        self.image_path = image_path  # Store path
        img = Image.open(image_path)
        self.img = img  # Store the original image for cropping
        preview_img = img.copy()
        preview_img.thumbnail((600, 400))  # Scale for preview
        self.tk_img = ImageTk.PhotoImage(preview_img)
        self.scaled_img = preview_img  # Save the scaled image
        width, height = preview_img.size
        self.canvas.config(width=width, height=height)
        self.canvas.delete("all")
        self.canvas_img = self.canvas.create_image(0, 0, image=self.tk_img, anchor="nw")
        self.canvas.image = self.tk_img
        self.rect = None  # Remove selection rect if any

    def on_click(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y, outline="red"
        )

    def on_drag(self, event):
        if self.rect:
            self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)
            self.crop_btn.config(state="normal")

    def save_crop(self):
        # Get selection coordinates on the preview image (canvas)
        x1, y1, x2, y2 = map(int, self.canvas.coords(self.rect))

        # Compute scaling factors
        original_width, original_height = self.img.size
        preview_width, preview_height = self.scaled_img.size
        fx = original_width / preview_width
        fy = original_height / preview_height

        # Map preview (canvas) coordinates back to original image
        crop_box = (
            int(min(x1, x2) * fx),
            int(min(y1, y2) * fy),
            int(max(x1, x2) * fx),
            int(max(y1, y2) * fy),
        )

        cropped = self.img.crop(crop_box)
        self.controller.cropped_image = cropped
        self.status.config(text="✅ Cropped image saved.")
        cropped.save("cropped.png")
        self.proceed_btn.config(state="normal")

    def proceed(self):
        self.controller.show_frame(Result)
