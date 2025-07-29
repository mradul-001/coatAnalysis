import tkinter as tk
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from app.utils.otsuBin import otsuBinarization
from app.utils.contours import findContours
from app.utils.noise import removeNoise
from app.utils.calculation import calculateWidth
import cv2


class Result(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        tk.Label(self, text="Processed Results", font=("Avenis", 18), bg="#f0f0f0").pack(pady=10)
        self.plot_frame = tk.Frame(self, bg="#f0f0f0")
        self.plot_frame.pack()
        self.result_label = tk.Label(self, text="", bg="#f0f0f0", font=("Avenis", 16))
        self.result_label.pack(pady=15)
        self.process_btn = tk.Button(self, text="Run Processing", font=("Avenis", 16), command=self.process_image)
        self.process_btn.pack(pady=10)

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.result_label.config(text="")
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

    def process_image(self):
        img = self.controller.cropped_image
        if not img:
            self.result_label.config(text="❌ No cropped image found.")
            return
        img_np = np.array(img.convert("L"))  # Ensure correct format

        # Step 1: Otsu Binarization
        t_img = otsuBinarization(img_np)

        # Step 2: Contour Detection
        contour_img, contours = findContours(t_img)

        # Step 3: Show Contour Image
        # fig1 = plt.figure(figsize=(6, 4))
        # plt.imshow(contour_img)
        # plt.axis('off')
        # plt.title("Detected Contours")
        # self._embed_figure(fig1)

        # Step 4: Noise Removal
        final_img = removeNoise(t_img, contours)

        # # Step 5: Show Filtered Image
        fig2 = plt.figure(figsize=(6, 2))
        plt.imshow(final_img, cmap='gray')
        plt.axis('off')
        plt.title("Cleaned Image")
        self._embed_figure(fig2)

        plt.imsave("output.png", final_img)

        # plt.clf()  # clear any previous plots

        # fig2 = plt.figure(figsize=(12, 6))  # bigger for full image
        # plt.imshow(final_img, cmap='gray')
        # plt.axis('off')
        # plt.title("Cleaned Image")
        # plt.tight_layout()  # ✅ ensure full image fits

        # self._embed_figure(fig2)
        # plt.close(fig2)  # ✅ cleanup

        # Step 6: Width Calculation
        width, variation = calculateWidth(final_img, self.controller.scale)

        self.result_label.config(
            text=f"Average Coating Thickness: {width:.2f} µm\n"
        )


    def _embed_figure(self, fig):
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)
