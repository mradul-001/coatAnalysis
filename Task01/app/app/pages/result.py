# import tkinter as tk
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import numpy as np
# from app.utils.bfs import region_growing_adaptive
# from app.utils.calculation import calculateWidth

# class Result(tk.Frame):
#     def __init__(self, parent, controller):
#         super().__init__(parent, bg="#f0f0f0")
#         self.controller = controller
        
#         tk.Label(self, text="Processed Results", font=("Avenis", 18), bg="#f0f0f0").pack(pady=10)
        
#         self.plot_frame = tk.Frame(self, bg="#f0f0f0")
#         self.plot_frame.pack()
        
#         self.result_label = tk.Label(self, text="", bg="#f0f0f0", font=("Avenis", 16))
#         self.result_label.pack(pady=15)
        
#         self.process_btn = tk.Button(self, text="Run Full Analysis", font=("Avenis", 16), command=self.process_all_images)
#         self.process_btn.pack(pady=10)

#     def tkraise(self, aboveThis=None):
#         super().tkraise(aboveThis)
#         self.result_label.config(text="")
#         for widget in self.plot_frame.winfo_children():
#             widget.destroy()

#     def process_all_images(self):
#         for widget in self.plot_frame.winfo_children():
#             widget.destroy()
#         self.result_label.config(text="Processing all images, please wait...")
#         self.update_idletasks()

#         images = self.controller.cropped_images
#         seeds_per_image = self.controller.seed_points_per_image
#         scale = self.controller.scale

#         if not images or not seeds_per_image:
#             self.result_label.config(text="Error: No cropped images or seeds found.")
#             return
#         if scale is None or scale == 0:
#             self.result_label.config(text="Error: Scale was not set correctly.")
#             return

#         total_weighted_thickness = 0
#         total_width_pixels = 0
#         individual_results = []

#         # Setup plot for individual results
#         num_images = len(images)
#         fig, axes = plt.subplots(num_images, 1, figsize=(8, 3 * num_images))
#         if num_images == 1: # Make sure axes is always a list
#             axes = [axes]
#         fig.suptitle("Segmented Regions")

#         for i in range(num_images):
#             img_pil = images[i]
#             seeds = seeds_per_image[i]
#             img_np = np.array(img_pil.convert("L"))

#             segmented_mask = region_growing_adaptive(img_np, seeds, threshold=50)
            
#             # Display individual segmented mask
#             axes[i].imshow(segmented_mask, cmap='gray')
#             axes[i].set_title(f"Image {i+1}")
#             axes[i].axis('off')

#             if segmented_mask is None or np.sum(segmented_mask) == 0:
#                 individual_results.append(f"Image {i+1}: Segmentation failed.")
#                 continue

#             thickness, _ = calculateWidth(segmented_mask, scale)
#             image_width_pixels = img_pil.width
            
#             if thickness > 0:
#                 total_weighted_thickness += thickness * image_width_pixels
#                 total_width_pixels += image_width_pixels
#                 individual_results.append(f"Image {i+1}: Avg Thickness = {thickness:.2f} µm")
#             else:
#                 individual_results.append(f"Image {i+1}: Could not calculate thickness.")

#         self._embed_figure(fig)

#         # Calculate final weighted average
#         if total_width_pixels > 0:
#             final_avg_thickness = total_weighted_thickness / total_width_pixels
#             result_text = f"Final Weighted Average Thickness: {final_avg_thickness:.2f} µm\n\n"
#             result_text += "Individual Results:\n" + "\n".join(individual_results)
#         else:
#             result_text = "Analysis complete, but could not determine an overall thickness."

#         self.result_label.config(text=result_text, justify="left")

#     def _embed_figure(self, fig):
#         canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
#         canvas.draw()
#         canvas.get_tk_widget().pack(pady=10, fill="both", expand=True)



import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from app.utils.bfs import region_growing_adaptive
from app.utils.calculation import calculateWidth

class Result(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        
        # --- UI Elements ---
        tk.Label(self, text="Analysis & Results", font=("Avenis", 18), bg="#f0f0f0").pack(pady=10)
        
        # A container for the scrollable area
        container = tk.Frame(self, bg="#f0f0f0")
        container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Canvas for scrolling
        canvas = tk.Canvas(container, bg="#f0f0f0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        
        # This frame will hold all the image plots and checkboxes
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Final result display label
        self.result_label = tk.Label(self, text="Select images to include in the final calculation.", bg="#f0f0f0", font=("Avenis", 16), wraplength=1000)
        self.result_label.pack(pady=15, padx=20)
        
        # The button to trigger the final calculation
        self.calculate_btn = tk.Button(
            self, 
            text="Calculate Final Thickness", 
            font=("Avenis", 16), 
            command=self.calculate_final_result,
            state="disabled"
        )
        self.calculate_btn.pack(pady=10, padx=20)

        # --- State Variables ---
        self.checkbox_vars = []
        self.individual_results_data = []

    def tkraise(self, aboveThis=None):
        """Called when the page is raised. Triggers the initial processing."""
        super().tkraise(aboveThis)
        self._initial_process_and_display()

    def _initial_process_and_display(self):
        """
        Processes all images, displays them with checkboxes, and stores
        the intermediate results.
        """
        # 1. Clear previous state and UI
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.checkbox_vars.clear()
        self.individual_results_data.clear()
        self.result_label.config(text="Processing all images, please wait...")
        self.calculate_btn.config(state="disabled")
        self.update_idletasks()

        # 2. Get data from the controller
        images = getattr(self.controller, 'cropped_images', [])
        seeds_per_image = getattr(self.controller, 'seed_points_per_image', [])
        scale = getattr(self.controller, 'scale', 0)

        if not images or not seeds_per_image or not scale:
            self.result_label.config(text="Error: Missing data (images, seeds, or scale). Please go back.")
            return

        # 3. Process each image
        for i, (img_pil, seeds) in enumerate(zip(images, seeds_per_image)):
            # Create a sub-frame for each result
            item_frame = tk.Frame(self.scrollable_frame, bg="#e9e9e9", bd=2, relief="groove")
            item_frame.pack(pady=10, padx=10, fill="x", expand=True)
            
            img_np = np.array(img_pil.convert("L"))
            segmented_mask = region_growing_adaptive(img_np, seeds, threshold=50)
            
            # Calculate individual thickness and store it
            thickness, _ = calculateWidth(segmented_mask, scale)
            image_width_pixels = img_pil.width
            self.individual_results_data.append({'thickness': thickness, 'width_pixels': image_width_pixels})

            # Create Checkbutton
            check_var = tk.IntVar(value=1 if thickness > 0 else 0) # Pre-select if valid
            self.checkbox_vars.append(check_var)
            
            check = tk.Checkbutton(
                item_frame, 
                text=f"Include Image {i+1} (Thickness: {thickness:.2f} µm)",
                variable=check_var,
                font=("Avenis", 12),
                bg="#e9e9e9"
            )
            check.pack(pady=5)
            if thickness <= 0:
                check.config(text=f"Image {i+1}: Invalid segmentation, excluded.", state="disabled")

            # Display the segmented mask
            fig = plt.figure(figsize=(8, 2))
            plt.imshow(segmented_mask, cmap='gray')
            plt.axis('off')
            canvas = FigureCanvasTkAgg(fig, master=item_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=5, padx=10)
            plt.close(fig) # Prevent memory leaks

        # 4. Finalize UI
        self.calculate_btn.config(state="normal")
        self.result_label.config(text="Select the images to include in the final calculation, then press the button below.")

    def calculate_final_result(self):
        """
        Calculates the final weighted average thickness based on user selection.
        """
        total_weighted_thickness = 0
        total_width_pixels = 0
        num_selected = 0

        for i, check_var in enumerate(self.checkbox_vars):
            if check_var.get() == 1: # If the checkbox is checked
                num_selected += 1
                result_data = self.individual_results_data[i]
                total_weighted_thickness += result_data['thickness'] * result_data['width_pixels']
                total_width_pixels += result_data['width_pixels']
        
        if total_width_pixels > 0:
            final_avg_thickness = total_weighted_thickness / total_width_pixels
            result_text = f"Final Weighted Average Thickness ({num_selected} images): {final_avg_thickness:.2f} µm"
        else:
            result_text = "No valid images were selected for calculation."

        self.result_label.config(text=result_text)
