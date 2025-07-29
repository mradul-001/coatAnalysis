import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from app.pages.scaleSelection import ScaleSelection

class ImageSelect(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")

        self.controller = controller
        tk.Label(
            self,
            text="Please upload an image showing the metal-coating interface.",
            font=("Avenis", 16),
            bg="#f0f0f0"
        ).pack(padx=24, pady=(40, 10))
        self.img_label = tk.Label(self, bg="#f0f0f0")
        self.img_label.pack(pady=20)

        tk.Button(
            self, text="Select Image", font=("Avenis", 16), width=20, command=self.load_image
        ).pack(padx=24, pady=10)



    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )
        if file_path:
            self.controller.image_path = file_path
            self.controller.frames[ScaleSelection].load_image(file_path)
            img = Image.open(file_path)
            preview_img = img.copy()
            preview_img.thumbnail((600, 400))  # adjust size as needed
            self.tk_img = ImageTk.PhotoImage(preview_img)

            self.img_label.config(image=self.tk_img)

            if not hasattr(self, "proceed_button"):
                self.proceed_button = tk.Button(
                    self,
                    text="Proceed",
                    font=("Avenis", 16),
                    width=20,
                    command=lambda: self.controller.show_frame(ScaleSelection),
                )
                self.proceed_button.pack(padx=24, pady=0)