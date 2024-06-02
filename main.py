# The main file for the desktop application
import pyglet, sqlite3, csv, sys, logging, os
import tkinter as tk
from PIL import Image, ImageTk

# Suppress TensorFlow logging
logging.getLogger('tensorflow').disabled = True
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from keras.models import load_model # type: ignore



# CONSTANTS
DB_NAME = "filmception.db"
bgColor = "#545454" # Gray
txtColor = "#FFFFFF" # White

pyglet.font.add_file("fonts/CaviarDreams.ttf")
pyglet.font.add_file("fonts/ArsenicaTrial-Regular.ttf")

# Main function
def createWindow():
    # Create the main window 
    window = tk.Tk()
    window.title("FilmCeption")
    window.geometry("720x640")
    window.iconphoto(False, tk.PhotoImage(file="img/icon.png"))
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
    searchBox = tk.Entry(mainFrame, width=40, font=("Ubuntu Regular", 12), bg=bgColor, fg=txtColor)
    searchBox.pack(pady=20)

    # Create Search Button beside the Search Box
    searchButton = tk.Button(mainFrame, text="Search", font=("Ubuntu Regular", 12), bg=bgColor, fg=txtColor, highlightthickness = 0)
    searchButton.pack(pady=20)

    # Get the text from the search box and search for the movie
    searchButton.config(command=lambda: findMovie(window, searchBox.get()))

    # Center the label and buttons
    mainFrame.update_idletasks()

    subLabelWidth = subLabel.winfo_width()
    subLabelX = (mainFrame.winfo_width() // 2) - (subLabelWidth // 2)
    subLabel.place(x=subLabelX, y=100)

    searchButtonWidth = searchButton.winfo_width()
    searchBoxWidth = searchBox.winfo_width()
    searchButtonX = (mainFrame.winfo_width() // 2) - (searchButtonWidth // 2)
    searchBoxX = (mainFrame.winfo_width() // 2) - (searchBoxWidth // 2)
    searchButton.place(x=searchButtonX, y=190)
    searchBox.place(x=searchBoxX, y=155)

    # Run the main loop
    window.mainloop()

    return window

# Find Movie function
def findMovie(window, movieName):
    print(f"Find Movie: {movieName}")
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Search for the movie sorted by year in descending order
    c.execute("SELECT * FROM films WHERE title LIKE ? ORDER BY year DESC", (f"%{movieName}%",))
    # Get the results of the search in paginated form
    results = c.fetchall()

    # Call the searchResults function
    searchResults(window, results)

    # Close the connection
    conn.close()

def onFrameConfigure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))

# Search results window function
def searchResults(window, results):

    # Update contents of the window to show a Search Box, a Search Button, and a Results Box
    # Create the main frame
    mainFrame = tk.Frame(window, width=720, height=640, bg=bgColor)
    mainFrame.grid(row=0, column=0)
    mainFrame.pack_propagate(False)

    # Create the main label and sub label, and pack them closely together
    subLabel = tk.Label(mainFrame, text="Movie Results", font=("Caviar Dreams", 32), bg=bgColor, fg=txtColor)
    subLabel.pack(pady=10)

    # Create a button for each result with the poster and title
    images = []
    
    # Create a scrollable frame for the results
    canvas = tk.Canvas(mainFrame, bg=bgColor)
    canvas.pack(side="top", fill="both", expand=True, pady=10)

    resultsFrame = tk.Frame(canvas, bg=bgColor)
    resultsFrame.pack(fill="both", expand=True)

    scrollbar = tk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.create_window((0,0), window=resultsFrame, anchor="nw")
    resultsFrame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

    counter = 0
    for result in results:
        # Load the poster
        poster = Image.open(f"img/posters/{result[0]}.jpg").resize((80,100))
        poster = ImageTk.PhotoImage(poster)
        images.append(poster)

        tempDate = result[2].split("-")[0]
        tempString = f"{result[1]} ({tempDate})"
        tk.Button(resultsFrame, image=poster).grid(row=counter, column=0)
        tk.Label(resultsFrame, text=tempString, font=("Ubuntu Regular", 12), bg=bgColor, fg=txtColor).grid(row=counter, column=1)
        
        counter += 1
        
    # Create the back button
    backButton = tk.Button(mainFrame, text="Back", font=("Ubuntu Regular", 12), bg=bgColor, fg=txtColor, highlightthickness = 0)
    backButton.pack(pady=20)

    # Back button command
    backButton.config(command=lambda: searchMovie(window))

    # Center the label and buttons
    mainFrame.update_idletasks()
    
    # Run the main loop
    window.mainloop()

    return window

    
# Show Movie function
def showMovie(window, movie):
    print("Show Movie")

# Upload Poster function
def uploadPoster():
    print("Upload Poster")

# Initialize the database
def initializeDB():
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Create the tables
    if c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='films'").fetchone():
        print("Database already initialized!")
        print("Reinitializing database...")

    c.execute("DROP TABLE films")
    c.execute("CREATE TABLE films (id INTEGER PRIMARY KEY, title TEXT, year TEXT, director TEXT, synopsis TEXT, poster TEXT, genre TEXT)")
    print("Database reinitialized successfully!")

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

    # Populate the database
    populateDB()

# Populate the database
def populateDB():
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Open the CSV file containing the movie data
    with open("films.csv", "r") as file:
        # Set the count of the rows then reset the file pointer
        counter = 0
        reader = csv.reader(file)
        len_reader = len(list(reader))
        file.seek(0)
        next(reader)

        # Insert the data into the database
        for row in reader:
            # print(f"[{counter+1}/{len_reader}] Current row: {row[1]}")
            c.execute("INSERT INTO films (id, title, year, director, synopsis, poster, genre) VALUES (?, ?, ?, ?, ?, ?, ?)", (row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
            counter += 1

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

# Preload the model
def preloadModel(model: str):
    if model == "vgg16":
        print("Preloading VGG16 model...")
        return load_model("models/vgg16-v2.keras")
    elif model == "xception":
        print("Preloading Xception model...")
        return load_model("models/xception-v2.keras")
    else:
        print("Invalid model!")
        sys.exit(1)
    

# Main function
if __name__ == "__main__":
    # Get the model from the arguments
    if len(sys.argv) < 2:
        print("Usage: python main.py <model>")
        # sys.exit(1)
        sys.argv.append("xception")
    model = preloadModel(sys.argv[1])


    # Initialize the database
    initializeDB()

    # Create the main window
    mainFrame = createWindow()
    
