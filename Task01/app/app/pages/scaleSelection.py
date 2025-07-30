import tkinter as tk
from PIL import Image, ImageTk
import math
from app.pages.crop import CropImage


class ScaleSelection(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        self.clicks = []

        tk.Label(self, text="Select Scale Bar", font=("Avenis", 24), bg="#f0f0f0").pack(
            pady=10
        )

        instr = (
            "Instructions:\n"
            "1. Enter the real-world length of the scale bar (e.g., 150 µm).\n"
            "2. Click on both ends of the scale bar in the image.\n"
            "3. The app will compute the scale (microns per pixel)."
        )
        tk.Label(
            self,
            text=instr,
            font=("Avenis", 16),
            bg="#f0f0f0",
            justify="left",
            anchor="w",
        ).pack(padx=30, pady=5, fill="x")

        self.entry_frame = tk.Frame(self, bg="#f0f0f0")
        self.entry_frame.pack(pady=5)
        tk.Label(self.entry_frame, text="Scale Length (µm):", bg="#f0f0f0").pack(
            side="left"
        )
        self.scale_entry = tk.Entry(self.entry_frame, width=10)
        self.scale_entry.pack(side="left", padx=5)

        self.canvas = tk.Canvas(self, bg="#ddd")
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.record_click)

        self.status = tk.Label(self, text="", bg="#f0f0f0", font=("Avenis", 16))
        self.status.pack()
        self.proceed_button = None

    def load_image(self, image_path):
        self.clicks.clear()
        self.status.config(text="")
        self.image_path = image_path

        img = Image.open(image_path)
        preview_img = img.copy()
        preview_img.thumbnail((1000, 800))
        self.tk_img = ImageTk.PhotoImage(preview_img)
        width, height = preview_img.size

        if hasattr(self, "canvas"):
            self.canvas.config(width=width, height=height)
            self.canvas.delete("all")
        else:
            self.canvas = tk.Canvas(self, width=width, height=height, bg="#ddd")
            self.canvas.pack(pady=10)
            self.canvas.bind("<Button-1>", self.record_click)

        self.canvas.create_image(0, 0, image=self.tk_img, anchor="nw")


    def record_click(self, event):
        self.clicks.append((event.x, event.y))
        self.canvas.create_oval(
            event.x - 3,
            event.y - 3,
            event.x + 3,
            event.y + 3,
            fill="red",
            outline="black",
        )

        if len(self.clicks) == 2:
            try:
                scale_real = float(self.scale_entry.get())
            except ValueError:
                self.status.config(
                    text="⚠️ Please enter a valid number for scale length."
                )
                return

            x1, y1 = self.clicks[0]
            x2, y2 = self.clicks[1]
            pixel_dist = math.hypot(x2 - x1, y2 - y1)

            if pixel_dist == 0:
                self.status.config(text="⚠️ Scale bar length cannot be zero.")
                return

            micron_per_pixel = scale_real / pixel_dist
            self.controller.scale = micron_per_pixel
            self.status.config(
                text=f"Scale: {micron_per_pixel:.4f} µm/pixel", font=("Avenis", 16)
            )

            if not self.proceed_button:
                self.proceed_button = tk.Button(
                    self,
                    text="Proceed",
                    font=("Avenis", 16),
                    width=20,
                    command=lambda: self.controller.show_frame(CropImage),
                )
                self.proceed_button.pack(padx=24, pady=10)
