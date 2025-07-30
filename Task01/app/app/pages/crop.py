import tkinter as tk
from PIL import Image, ImageTk
from app.pages.seedSelection import SelectSeed

class CropImage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        self.rect = None
        self.start_x = self.start_y = 0
        self.crop_rects_coords = [] # Stores coordinates of drawn rectangles
        self.crop_rects_on_canvas = [] # Stores canvas rectangle objects

        tk.Label(
            self, text="Draw and Add one or more Crop Regions", font=("Avenis", 18), bg="#f0f0f0"
        ).pack(pady=10)

        self.canvas = tk.Canvas(self, bg="#ddd", cursor="cross")
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)

        self.status = tk.Label(self, text="No crop regions added.", bg="#f0f0f0")
        self.status.pack()

        # --- Button Frame ---
        self.button_frame = tk.Frame(self, bg="#f0f0f0")
        self.button_frame.pack(pady=10)
        
        self.add_crop_btn = tk.Button(
            self.button_frame,
            text="Add Crop Region",
            font=("Avenis", 16),
            command=self.add_crop,
            state="disabled",
        )
        self.add_crop_btn.pack(side="left", padx=10)

        self.reset_btn = tk.Button(
            self.button_frame,
            text="Reset All",
            font=("Avenis", 16),
            command=self.reset_crops
        )
        self.reset_btn.pack(side="left", padx=10)

        self.proceed_btn = tk.Button(
            self.button_frame,
            text="Confirm Crops & Proceed",
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
        self.reset_crops()
        self.image_path = image_path
        img = Image.open(image_path)
        self.img = img
        
        preview_img = img.copy()
        preview_img.thumbnail((1000, 800))
        self.tk_img = ImageTk.PhotoImage(preview_img)
        self.scaled_img = preview_img
        
        width, height = preview_img.size
        self.canvas.config(width=width, height=height)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.tk_img, anchor="nw")
        self.canvas.image = self.tk_img
        self.rect = None

    def on_click(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y, outline="red", width=2
        )

    def on_drag(self, event):
        if self.rect:
            self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)
            self.add_crop_btn.config(state="normal")

    def add_crop(self):
        if not self.rect:
            return
            
        coords = self.canvas.coords(self.rect)
        self.crop_rects_coords.append(coords)
        
        # Make the saved rectangle permanent and green
        perm_rect = self.canvas.create_rectangle(coords, outline="green", width=2)
        self.crop_rects_on_canvas.append(perm_rect)
        
        # Delete the temporary red rectangle
        self.canvas.delete(self.rect)
        self.rect = None
        
        self.status.config(text=f"{len(self.crop_rects_coords)} crop region(s) added.")
        self.proceed_btn.config(state="normal")
        self.add_crop_btn.config(state="disabled")

    def reset_crops(self):
        self.crop_rects_coords.clear()
        for r in self.crop_rects_on_canvas:
            self.canvas.delete(r)
        self.crop_rects_on_canvas.clear()
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = None
        self.status.config(text="No crop regions added.")
        self.proceed_btn.config(state="disabled")
        self.add_crop_btn.config(state="disabled")

    def proceed(self):
        cropped_images = []
        original_width, original_height = self.img.size
        preview_width, preview_height = self.scaled_img.size
        fx = original_width / preview_width
        fy = original_height / preview_height

        for coords in self.crop_rects_coords:
            x1, y1, x2, y2 = coords
            crop_box = (
                int(min(x1, x2) * fx),
                int(min(y1, y2) * fy),
                int(max(x1, x2) * fx),
                int(max(y1, y2) * fy),
            )
            cropped = self.img.crop(crop_box)
            cropped_images.append(cropped)
            
        self.controller.cropped_images = cropped_images
        self.controller.show_frame(SelectSeed)
