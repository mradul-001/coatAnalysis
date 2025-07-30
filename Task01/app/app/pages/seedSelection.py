import tkinter as tk
from PIL import Image, ImageTk
from app.pages.result import Result

class SelectSeed(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        self.tk_img = None
        self.current_image_index = 0
        self.seed_points_per_image = []

        # --- Widgets ---
        self.title_label = tk.Label(self, text="", font=("Avenis", 18), bg="#f0f0f0")
        self.title_label.pack(pady=10)

        self.canvas = tk.Canvas(self, bg="#ddd", cursor="cross")
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.record_seed)

        self.status = tk.Label(self, text="", bg="#f0f0f0", font=("Avenis", 12))
        self.status.pack(pady=5)
        
        # --- Navigation and Action Frame ---
        nav_frame = tk.Frame(self, bg="#f0f0f0")
        nav_frame.pack(pady=10)

        self.prev_btn = tk.Button(nav_frame, text="<< Prev Image", font=("Avenis", 16), command=self.prev_image)
        self.prev_btn.pack(side="left", padx=10)

        self.reset_btn = tk.Button(nav_frame, text="Reset Points for this Image", font=("Avenis", 16), command=self.reset_points_for_current_image)
        self.reset_btn.pack(side="left", padx=10)

        self.proceed_btn = tk.Button(nav_frame, text="Confirm All Seeds & Proceed", font=("Avenis", 16), command=self.proceed, state="disabled")
        self.proceed_btn.pack(side="left", padx=10)

        self.next_btn = tk.Button(nav_frame, text="Next Image >>", font=("Avenis", 16), command=self.next_image)
        self.next_btn.pack(side="left", padx=10)

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        if hasattr(self.controller, "cropped_images") and self.controller.cropped_images:
            num_images = len(self.controller.cropped_images)
            self.seed_points_per_image = [[] for _ in range(num_images)]
            self.current_image_index = 0
            self.load_image_at_index(self.current_image_index)
        else:
            self.title_label.config(text="Error: No cropped images found.")

    def load_image_at_index(self, index):
        num_images = len(self.controller.cropped_images)
        self.title_label.config(text=f"Select seeds for Image {index + 1} of {num_images}")
        
        img = self.controller.cropped_images[index]
        preview_img = img.copy()
        preview_img.thumbnail((800, 600))
        self.tk_img = ImageTk.PhotoImage(preview_img)
        
        self.canvas.config(width=preview_img.width, height=preview_img.height)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.tk_img, anchor="nw")
        self.canvas.image = self.tk_img

        # Redraw seeds for this image
        for y, x in self.seed_points_per_image[index]:
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="blue", outline="white")
        
        self.update_status_and_buttons()

    def record_seed(self, event):
        x, y = event.x, event.y
        self.seed_points_per_image[self.current_image_index].append((y, x))
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="blue", outline="white")
        self.update_status_and_buttons()

    def reset_points_for_current_image(self):
        self.seed_points_per_image[self.current_image_index].clear()
        self.load_image_at_index(self.current_image_index) # Reload to clear canvas

    def prev_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.load_image_at_index(self.current_image_index)

    def next_image(self):
        num_images = len(self.controller.cropped_images)
        if self.current_image_index < num_images - 1:
            self.current_image_index += 1
            self.load_image_at_index(self.current_image_index)

    def update_status_and_buttons(self):
        num_images = len(self.controller.cropped_images)
        
        # Update status label
        num_seeds = len(self.seed_points_per_image[self.current_image_index])
        self.status.config(text=f"{num_seeds} seed(s) selected for this image.")
        
        # Update nav buttons
        self.prev_btn.config(state="normal" if self.current_image_index > 0 else "disabled")
        self.next_btn.config(state="normal" if self.current_image_index < num_images - 1 else "disabled")
        
        # Update proceed button (enabled only if every image has at least one seed)
        all_have_seeds = all(len(seeds) > 0 for seeds in self.seed_points_per_image)
        self.proceed_btn.config(state="normal" if all_have_seeds else "disabled")

    def proceed(self):
        self.controller.seed_points_per_image = self.seed_points_per_image
        self.controller.show_frame(Result)
