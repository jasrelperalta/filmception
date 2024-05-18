# The main file for the desktop application

import tkinter as tk
import pyglet
import sqlite3

# CONSTANTS
DB_NAME = "filmception.db"
bgColor = "#545454" # Gray
txtColor = "#FFFFFF" # White

pyglet.font.add_file("filmception/fonts/CaviarDreams.ttf")
pyglet.font.add_file("filmception/fonts/ArsenicaTrial-Regular.ttf")

# Main function
def createWindow():
    # Create the main window 
    window = tk.Tk()
    window.title("FilmCeption")
    window.geometry("720x640")
    window.iconphoto(False, tk.PhotoImage(file="filmception/img/icon.png"))
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


    # Create the main label and sub label, and pack them closely together
    subLabel = tk.Label(mainFrame, text="Welcome to", font=("Caviar Dreams", 32), bg=bgColor, fg=txtColor)
    mainLabel = tk.Label(mainFrame, text="FilmCeption!", font=("Arsenica Trial", 64), bg=bgColor, fg="#ff5454")
    subLabel.pack(pady=10)
    mainLabel.pack(pady=10)


    # Create buttons
    # Search Movie button
    searchButton = tk.Button(mainFrame, text="Movie Search", font=("Ubuntu Regular", 12), bg=bgColor, fg=txtColor, highlightthickness = 0, bd = 0)
    searchButton.pack(pady=20)

    # Search Movie button command
    searchButton.config(command=lambda: searchMovie(mainFrame))

    # Upload Poster button
    uploadButton = tk.Button(mainFrame, text="Upload Poster", font=("Ubuntu Regular", 12), bg=bgColor, fg=txtColor, highlightthickness = 0, bd = 0)
    uploadButton.pack(pady=20)

    # Upload Poster button command
    uploadButton.config(command=uploadPoster)

    # Center the buttons
    mainFrame.update_idletasks()

    # Center the label and buttons
    mainLabelWidth = mainLabel.winfo_width()
    subLabelWidth = subLabel.winfo_width()
    mainLabelX = (mainFrame.winfo_width() // 2) - (mainLabelWidth // 2)
    subLabelX = (mainFrame.winfo_width() // 2) - (subLabelWidth // 2)
    mainLabel.place(x=mainLabelX, y=150)
    subLabel.place(x=subLabelX, y=100)

    searchButtonWidth = searchButton.winfo_width()
    uploadButtonWidth = uploadButton.winfo_width()
    searchButtonX = (mainFrame.winfo_width() // 2) - (searchButtonWidth // 2)
    uploadButtonX = (mainFrame.winfo_width() // 2) - (uploadButtonWidth // 2)
    searchButton.place(x=searchButtonX, y=350)
    uploadButton.place(x=uploadButtonX, y=400)

    # Run the main loop
    window.mainloop()

    return window

# Search Movie function
def searchMovie(window):
    print("Search Movie")
    # Update contents of the window to show a Search Box, a Search Button, and a Results Box
    # Create the main frame
    mainFrame = tk.Frame(window, width=720, height=640, bg=bgColor)
    mainFrame.grid(row=0, column=0)
    mainFrame.pack_propagate(False)

    # Create the main label and sub label, and pack them closely together
    subLabel = tk.Label(mainFrame, text="Search for a movie", font=("Caviar Dreams", 32), bg=bgColor, fg=txtColor)
    subLabel.pack(pady=10)

    # Create Search Box
    SearchBox = tk.Entry(mainFrame, width=40, font=("Ubuntu Regular", 12), bg=bgColor, fg=txtColor)
    SearchBox.pack(pady=20)

    # Create Search Button beside the Search Box
    searchButton = tk.Button(mainFrame, text="Search", font=("Ubuntu Regular", 12), bg=bgColor, fg=txtColor, highlightthickness = 0)
    searchButton.pack(pady=20)

    # Create Results Box
    resultsBox = tk.Label(mainFrame, text="Results", font=("Ubuntu Regular", 12), bg=bgColor, fg=txtColor)
    resultsBox.pack(pady=20)

    # Center the label and buttons
    mainFrame.update_idletasks()

    subLabelWidth = subLabel.winfo_width()
    subLabelX = (mainFrame.winfo_width() // 2) - (subLabelWidth // 2)
    subLabel.place(x=subLabelX, y=100)

    searchButtonWidth = searchButton.winfo_width()
    searchBoxWidth = SearchBox.winfo_width()
    searchButtonX = (mainFrame.winfo_width() // 2) - (searchButtonWidth // 2)
    searchBoxX = (mainFrame.winfo_width() // 2) - (searchBoxWidth // 2)
    searchButton.place(x=searchButtonX, y=190)
    SearchBox.place(x=searchBoxX, y=155)

    # Run the main loop
    window.mainloop()

    return window


# Search Button
    # Results Box


# Upload Poster function
def uploadPoster():
    print("Upload Poster")

if __name__ == "__main__":
    mainFrame = createWindow()
    
