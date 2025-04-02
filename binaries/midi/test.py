import os
import tkinter as tk
from tkinter import PhotoImage

# Debugging: print the current working directory
print("Current Working Directory:", os.getcwd())

# Set the working directory to the script's directory (in case it's different)
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Try loading the PNG image
try:
    bg_image = PhotoImage(file="background.png")
    print("Image loaded successfully.")
except Exception as e:
    print(f"Error loading image: {e}")

# Create the window
window = tk.Tk()
window.title("MIDI Cymbal Hit Detection")
window.geometry("500x500")

# Set background image
background_label = tk.Label(window, image=bg_image)
background_label.place(relwidth=1, relheight=1)  # Stretch it across the window

# Start the Tkinter event loop
window.mainloop()
