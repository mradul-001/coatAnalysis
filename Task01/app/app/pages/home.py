import tkinter as tk
from app.pages.imageSelect import ImageSelect


class Home(tk.Frame):
    def __init__(self, parent, controller):

        super().__init__(parent, bg="#f0f0f0")
        controller.geometry("1200x900") # Increased height for more text

        tk.Label(
            self,
            text="Metal Coating Thickness Estimator",
            font=("Avenis", 18),
            bg="#f0f0f0",
        ).pack(pady=25)

        instructions = (
            "Instructions for Using the Application:\n\n"
            "1. Upload an image that clearly shows the metal-coating interface.\n\n"
            "2. Select the scale bar from the uploaded image to calibrate measurements.\n\n"
            "3. Crop one or more regions of interest from the image.\n\n"
            "4. For each cropped region, select one or more 'seed points' inside the coating.\n\n"
            "5. The application will process each region and display the final weighted\n"
            "   average coating thickness."
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
            text="Start",
            font=("Avenis", 16),
            padx=24,
            pady=10,
            command=lambda: controller.show_frame(ImageSelect),
        ).pack(pady=25)
