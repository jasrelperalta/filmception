# The main file for the desktop application

import tkinter as tk
import sqlite3

# CONSTANTS
DB_NAME = "filmception.db"
bgColor = "#818589" # Gray
txtColor = "#FFFFFF" # White

# Main function
def createWindow():
    # Create the main window 
    window = tk.Tk()
    window.title("FilmCeption")
    window.geometry("720x640")
    window.resizable(False, False)

    # Center the window
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")
    
    # Create the main frame
    mainFrame = tk.Frame(window, width=720, height=640, bg=bgColor)
    mainFrame.grid(row=0, column=0)
    mainFrame.pack_propagate(False)

    # Create the main label
    mainLabel = tk.Label(mainFrame, text="Welcome to FilmCeption!", font=("Arial", 24), bg=bgColor, fg=txtColor)
    mainLabel.pack(pady=20)

    # Run the main loop
    window.mainloop()

if __name__ == "__main__":
    createWindow()