# Metal Coating Thickness Estimator

This application is a computer vision tool designed to analyze micrograph images of metal-coating interfaces and calculate the average thickness of the coating. It provides a graphical user interface (GUI) built with Python's Tkinter library to guide the user through the process of image calibration, cropping, and semi-automated segmentation.

The core of the application uses an adaptive region-growing (BFS) algorithm to segment the coating from the substrate, even in the presence of cracks and variations in brightness. The user can select multiple regions of interest and interactively choose which segmented parts contribute to the final thickness calculation, which is presented as a weighted average.

This tool was developed as part of a research project at the Indian Institute of Technology Bombay (IITB) under the guidance of **Prof. Soham Mujumdar**.


### Citation
A significant portion of the Python code in this project was developed with the assistance of Google's Gemini, a large language model.
* **Tool:** Google Gemini
* **Date of Interaction:** July 2025
* **Publisher:** Google
* **Prompts:** A series of conversational prompts regarding Python, Tkinter, and application architecture.
