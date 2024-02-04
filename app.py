import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import pytz
import json
import requests

# Define predefined messages
PREDEFINED_MESSAGES = {
    "Test": "This is a test.",
    "Hello": "Hello everyone!",
    "Important Announcement": "Please pay attention to this important announcement listed below.",
    "Temp Shutdown": 'The server will shut down for a bit.',
    "New Member": 'A new member joined the server, say hello! (:',
    "AFK Note": 'The server owner is AFK.',
    "New Video": 'A new video is coming out soon.',
    "Live Stream": 'Im streaming live on my channel right now, dont forget to watch it.',
    "Song Released": "I dropped a new song. Watch it NOW!",
    "Raid": "Server raid!",
    "Server Revamp": "This server is getting a revamp soon (:",
    "Listen to Rules": "Make sure to read the rules.",
    "Staff and Owner Online": "Our staff are active on our server right now.",
    "Staff Offline": "Our staff are not online right now.",
    "Moderation In Place": "Our server is being looked at right now for content that violates our rules"
}

# Define cooldown duration in seconds
COOLDOWN_DURATION = 5

# Load saved settings from file
try:
    with open("settings.json", "r") as file:
        settings = json.load(file)
except FileNotFoundError:
    settings = {"font_size": 16, "font_color": "black", "webhook_url": ""}

# Variable to track cooldown state, spam mode, and timestamp inclusion
cooldown_active = False
spam_mode_active = False
include_timestamp = True

# Function to handle sending predefined message button click
def send_predefined_message(message):
    send_message(message)

# Function to handle sending custom message
def send_custom_message():
    message = custom_message_entry.get("1.0", "end").strip()
    if message:
        send_message(message)
        custom_message_entry.delete("1.0", "end")
    else:
        messagebox.showerror("Error", "Please enter a message.")

# Function to send message via Discord webhook
def send_message(message):
    global cooldown_active
    
    if not settings["webhook_url"]:
        messagebox.showerror("Error", "Webhook URL is not set. Please set the webhook URL first.")
        return

    if not spam_mode_active and cooldown_active:
        messagebox.showerror("Error", f"Please wait for the cooldown period ({COOLDOWN_DURATION} seconds)")
        return

    if include_timestamp:
        est_timezone = pytz.timezone('US/Eastern')
        current_time = datetime.now(est_timezone).strftime("%Y-%m-%d %H:%M:%S")
        message = f"{current_time} EST: {message}"

    data = {"content": message}
    response = requests.post(settings["webhook_url"], json=data)

    if response.status_code == 204:
        messagebox.showinfo("Message Sent", "Message sent successfully!")
    else:
        messagebox.showerror("Error", "Failed to send message. Please try again later.")

    if not spam_mode_active:
        cooldown_active = True
        window.after(COOLDOWN_DURATION * 1000, reset_cooldown)

# Function to reset cooldown
def reset_cooldown():
    global cooldown_active
    cooldown_active = False

# Function to toggle spam mode
def toggle_spam_mode():
    global spam_mode_active
    spam_mode_active = not spam_mode_active
    if spam_mode_active:
        spam_mode_button.config(text="Spam Mode: ON", fg="green")
    else:
        spam_mode_button.config(text="Spam Mode: OFF", fg="red")

# Function to toggle timestamp inclusion
def toggle_timestamp():
    global include_timestamp
    include_timestamp = not include_timestamp
    if include_timestamp:
        timestamp_button.config(text="Timestamp: ON", fg="green")
    else:
        timestamp_button.config(text="Timestamp: OFF", fg="red")

# Function to change font size
def change_font_size(size):
    for widget in window.winfo_children():
        widget.config(font=("Helvetica", size))
    settings["font_size"] = size
    save_settings()

# Function to change font color
def change_font_color(color):
    for widget in window.winfo_children():
        widget.config(fg=color)
    settings["font_color"] = color
    save_settings()

# Function to save settings to file
def save_settings():
    with open("settings.json", "w") as file:
        json.dump(settings, file)

# Function to open a dialog to set the webhook URL
def set_webhook_url():
    url = simpledialog.askstring("Set Webhook URL", "Enter your Discord webhook URL:", parent=window)
    if url:
        settings["webhook_url"] = url
        save_settings()

# Create GUI window
window = tk.Tk()
window.title("Webhooker")

# Current time label
time_label = tk.Label(window, text="", font=("Helvetica", settings["font_size"]))
time_label.pack(pady=(10, 5))

# Label above the predefined messages
commands_label = tk.Label(window, text="Commands", font=("Helvetica", settings["font_size"]))
commands_label.pack()

# Create frame for predefined message buttons
predefined_message_buttons_frame = tk.Frame(window)
predefined_message_buttons_frame.pack(padx=10, pady=(0, 5), anchor="center")

# Calculate number of columns for grid layout
num_columns = 5
num_buttons = len(PREDEFINED_MESSAGES)
num_rows = (num_buttons + num_columns - 1) // num_columns

# Populate predefined messages in grid layout
predefined_message_buttons = []
for idx, (message, content) in enumerate(PREDEFINED_MESSAGES.items()):
    row = idx // num_columns
    col = idx % num_columns
    button = tk.Button(predefined_message_buttons_frame, text=message, font=("Helvetica", settings["font_size"]), command=lambda msg=content: send_predefined_message(msg))
    button.grid(row=row, column=col, padx=5, pady=2, sticky="nsew")  # Align buttons to center within each grid cell
    predefined_message_buttons.append(button)

# Configure grid columns to have uniform width
for col in range(num_columns):
    predefined_message_buttons_frame.grid_columnconfigure(col, weight=1, uniform="buttons")

# Option to change font size
font_size_frame = tk.Frame(window)
font_size_frame.pack(pady=(5, 0), anchor="center")

font_size_label = tk.Label(font_size_frame, text="Change Font Size:", font=("Helvetica", settings["font_size"]))
font_size_label.pack(side=tk.LEFT, padx=5)

font_size_dropdown = ttk.Combobox(font_size_frame, values=[8, 10, 12, 14, 16, 18, 20, 25, 30]) # Add other font sizes by adding numbers
font_size_dropdown.pack(side=tk.LEFT, padx=5)

font_size_dropdown.set(settings["font_size"])

def change_font_size_event(event):
    size = int(font_size_dropdown.get())
    change_font_size(size)

font_size_dropdown.bind("<<ComboboxSelected>>", change_font_size_event)

# Option to change font color
font_color_frame = tk.Frame(window)
font_color_frame.pack(pady=5, anchor="center")

font_color_label = tk.Label(font_color_frame, text="Change Font Color:", font=("Helvetica", settings["font_size"]))
font_color_label.pack(side=tk.LEFT, padx=5)

font_color_dropdown = ttk.Combobox(font_color_frame, values=["black", "red", "green", "blue", "yellow", "orange", "purple", "cyan", "magenta", "brown"])
font_color_dropdown.pack(side=tk.LEFT, padx=5)

font_color_dropdown.set(settings["font_color"])

def change_font_color_event(event):
    color = font_color_dropdown.get()
    change_font_color(color)

font_color_dropdown.bind("<<ComboboxSelected>>", change_font_color_event)

# Button to set webhook URL
set_webhook_button = tk.Button(window, text="Set Webhook URL", command=set_webhook_url, font=("Helvetica", settings["font_size"]))
set_webhook_button.pack(pady=(10, 5), anchor="center")

# Fullscreen button
fullscreen_button = tk.Button(window, text="Fullscreen", command=lambda: window.attributes("-fullscreen", not window.attributes("-fullscreen")), font=("Helvetica", settings["font_size"]))
fullscreen_button.pack(pady=5, anchor="center")

# Label above the custom message box
custom_message_label = tk.Label(window, text="Custom Messages", font=("Helvetica", settings["font_size"]))
custom_message_label.pack(pady=(5, 0))

# Frame for custom message entry
custom_message_frame = tk.Frame(window)
custom_message_frame.pack(pady=5, anchor="center")

# Scrollbar for custom message entry
custom_message_scrollbar = tk.Scrollbar(custom_message_frame)
custom_message_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Text box for custom message
custom_message_entry = tk.Text(custom_message_frame, height=4, width=50, font=("Helvetica", settings["font_size"]), yscrollcommand=custom_message_scrollbar.set)
custom_message_entry.pack(fill=tk.BOTH, expand=True)
custom_message_scrollbar.config(command=custom_message_entry.yview)

# Button to send custom message
send_custom_button = tk.Button(window, text="Send Custom Message", command=send_custom_message, font=("Helvetica", settings["font_size"]))
send_custom_button.pack(pady=5)

# Spam Mode button
spam_mode_button = tk.Button(window, text="Spam Mode: OFF", command=toggle_spam_mode, font=("Helvetica", settings["font_size"]), fg="red")
spam_mode_button.pack(pady=5, anchor="center")

# Timestamp button
timestamp_button = tk.Button(window, text="Timestamp: ON", command=toggle_timestamp, font=("Helvetica", settings["font_size"]), fg="green")
timestamp_button.pack(pady=5, anchor="center")

# Set initial window size
window.normal_width = min(window.winfo_screenwidth(), 800)
window.normal_height = min(window.winfo_screenheight(), 620)

# Start updating current time label immediately
def update_time_label():
    est_timezone = pytz.timezone('US/Eastern')
    current_time = datetime.now(est_timezone).strftime("%Y-%m-%d %H:%M:%S")
    time_label.config(text=current_time)
    window.after(1000, update_time_label)

update_time_label()

# Run the GUI
window.mainloop()
