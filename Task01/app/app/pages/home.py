import tkinter as tk
from app.pages.imageSelect import ImageSelect


class Home(tk.Frame):
    def __init__(self, parent, controller):

        super().__init__(parent, bg="#f0f0f0")
        controller.geometry("800x450")

        tk.Label(
            self,
            text="Metal Coating Thickness Estimator",
            font=("Avenis", 18),
            bg="#f0f0f0",
        ).pack(pady=25)

        instructions = (
            "Instructions for Using the Application:\n\n"
            "1. Upload an image that clearly shows the metal-coating interface.\n"
            "2. Select the scale bar from the uploaded image to calibrate measurements.\n"
            "3. Crop the region of interest containing the metal-coating interface.\n"
            "4. The application will process the selected region and display the results,\n"
            "    including the computed average coating thickness and its variation."
        )

        tk.Label(
            self,
            text=instructions,
            justify="left",
            font=("Avenis", 16),
            bg="#f0f0f0",
            anchor="w",
        ).pack(padx=40, pady=10, fill="both")

        tk.Button(
            self,
            text="Next",
            font=("Avenis", 16),
            padx=24,
            pady=10,
            command=lambda: controller.show_frame(
                controller.frames[ImageSelect].__class__
            ),
        ).pack(pady=25)
