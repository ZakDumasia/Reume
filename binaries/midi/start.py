import numpy as np
import sounddevice as sd
import mido
from mido import Message, open_output
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import PhotoImage

# Function to initialize MIDI output ports and create the MIDI output
def initialize_midi_output():
    available_ports = mido.get_output_names()
    if not available_ports:
        messagebox.showerror("Error", "No available MIDI output ports! Start loopMIDI first.")
        return None
    return available_ports

# Function to trigger MIDI note
def trigger_midi(note, velocity):
    """Send MIDI note to output"""
    msg = Message('note_on', note=note, velocity=velocity, channel=MIDI_CHANNEL)  # Channel 9 is standard for drums
    midi_out.send(msg)  # Send the MIDI message

# Callback to process audio input and send MIDI note when threshold is exceeded
def callback(indata, frames, time, status):
    """Detects cymbal hits and converts them to MIDI"""
    volume = np.max(np.abs(indata))  # Get the peak volume of the input
    if volume > THRESHOLD:
        velocity = min(int(volume * VELOCITY_SCALING), 127)
        trigger_midi(NOTE, velocity)
        status_var.set(f"Triggered: Note {NOTE} (Velocity: {velocity})")  # Update status

# Function to start listening to the audio input and MIDI output
def start_detection():
    global midi_out

    # Get the selected MIDI output port
    selected_port = midi_output_var.get()
    if not selected_port:
        messagebox.showerror("Error", "Please select a MIDI output port.")
        return

    # Open the selected MIDI output port
    try:
        midi_out = open_output(selected_port)
        status_var.set(f"Connected to MIDI Output: {selected_port}")
        print(f"Connected to MIDI Output: {selected_port}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open MIDI output: {e}")
        return

    # Start listening to the microphone input
    with sd.InputStream(device=1, channels=1, callback=callback, samplerate=44100):
        status_var.set("Listening for cymbal hits... Press Ctrl+C to exit.")
        print("Listening for cymbal hits...")

# Keep the window running forever to listen to the audio input
def listen_forever():
    window.after(1000, listen_forever)

# GUI Setup
window = tk.Tk()
window.title("MIDI Cymbal Hit Detection")
window.geometry("500x500")
window.config(bg="#222222")  # Set a dark background for VST look

# Load background texture (similar to WhatsApp's texture)
bg_image = PhotoImage(file="background.png")

background_label = tk.Label(window, image=bg_image)
background_label.place(relwidth=1, relheight=1)  # Stretch it across the window

# Configuration
MIDI_CHANNEL = 9  # Standard for drum MIDI
NOTE = 38  # General MIDI Crash Cymbal
VELOCITY_SCALING = 127  # Maximum MIDI velocity
THRESHOLD = 0.02  # Sensitivity threshold

# Variables
status_var = tk.StringVar()

# Header label with a VST-like feel
header_label = tk.Label(window, text="MIDI Cymbal Hit Detection", font=("Arial", 18, "bold"), fg="#FFFFFF", bg="#444444", relief="solid", padx=10, pady=10)
header_label.pack(pady=20, fill="x")

# Label for status with a VST-style border
status_label = tk.Label(window, textvariable=status_var, height=2, anchor="w", font=("Arial", 12), bg="#333333", fg="#FFFFFF", relief="solid", padx=15)
status_label.pack(padx=20, pady=10, fill="x")

# MIDI Output Section with a sleek frame and rounded borders
midi_output_frame = tk.LabelFrame(window, text="MIDI Output Configuration", padx=20, pady=10, fg="white", bg="#444444", font=("Arial", 12))
midi_output_frame.pack(padx=20, pady=10, fill="x")

# Dropdown for MIDI output ports (styled as a combobox)
available_ports = initialize_midi_output()
if available_ports:
    midi_output_var = tk.StringVar(window)
    midi_output_var.set(available_ports[0])  # Set default to the first available port

    midi_output_menu = ttk.Combobox(midi_output_frame, textvariable=midi_output_var, values=available_ports, state="readonly", font=("Arial", 12), width=30)
    midi_output_menu.pack(padx=10, pady=5)

# Start Detection Button with modern style
start_button = tk.Button(window, text="Start Detection", command=start_detection, width=20, height=2, bg="#4CAF50", fg="white", font=("Arial", 14, "bold"), relief="raised", bd=4)
start_button.pack(pady=30)

# Footer with instructions, styled with a gray color
footer_label = tk.Label(window, text="Ensure loopMIDI is running and your microphone is set up.", font=("Arial", 10), fg="gray", bg="#222222")
footer_label.pack(side="bottom", pady=10)

# Start the Tkinter event loop
window.mainloop()
