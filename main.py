# The main file for the desktop application
import pyglet, sqlite3, csv, sys, logging, os
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
from tkinter import filedialog

# Suppress TensorFlow logging
logging.getLogger('tensorflow').disabled = True
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from keras.models import load_model # type: ignore



# CONSTANTS
DB_NAME = "filmception.db"
bgColor = "#545454" # Gray
txtColor = "#FFFFFF" # White
genreList = ["Action", "Adventure", "Animation", "Comedy", "Crime", "Drama", "Fantasy", "Romance", "Thriller"]

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
    uploadButton.config(command=lambda: uploadPoster(mainFrame))

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

    # Initialize variables containing genre labels to be used for checkboxes
    actionCheck = tk.IntVar()
    adventureCheck = tk.IntVar()
    animationCheck = tk.IntVar()
    comedyCheck = tk.IntVar()
    crimeCheck = tk.IntVar()
    dramaCheck = tk.IntVar()
    fantasyCheck = tk.IntVar()
    romanceCheck = tk.IntVar()
    thrillerCheck = tk.IntVar()

    # Create the genre checkboxes
    actionBox = tk.Checkbutton(mainFrame, text="Action", variable=actionCheck, font=("Ubuntu Regular", 12), bg=bgColor, fg=txtColor, borderwidth=0, highlightthickness=0)
    actionBox.pack(pady=10)
    adventureBox = tk.Checkbutton(mainFrame, text="Adventure", variable=adventureCheck, font=("Ubuntu Regular", 12), bg=bgColor, fg=txtColor, borderwidth=0, highlightthickness=0)
    adventureBox.pack(pady=10)
    animationBox = tk.Checkbutton(mainFrame, text="Animation", variable=animationCheck, font=("Ubuntu Regular", 12), bg=bgColor, fg=txtColor, borderwidth=0, highlightthickness=0)
    animationBox.pack(pady=10)
    comedyBox = tk.Checkbutton(mainFrame, text="Comedy", variable=comedyCheck, font=("Ubuntu Regular", 12), bg=bgColor, fg=txtColor, borderwidth=0, highlightthickness=0)
    comedyBox.pack(pady=10)
    crimeBox = tk.Checkbutton(mainFrame, text="Crime", variable=crimeCheck, font=("Ubuntu Regular", 12), bg=bgColor, fg=txtColor, borderwidth=0, highlightthickness=0)
    crimeBox.pack(pady=10)
    dramaBox = tk.Checkbutton(mainFrame, text="Drama", variable=dramaCheck, font=("Ubuntu Regular", 12), bg=bgColor, fg=txtColor, borderwidth=0, highlightthickness=0)
    dramaBox.pack(pady=10)
    fantasyBox = tk.Checkbutton(mainFrame, text="Fantasy", variable=fantasyCheck, font=("Ubuntu Regular", 12), bg=bgColor, fg=txtColor, borderwidth=0, highlightthickness=0)
    fantasyBox.pack(pady=10)
    romanceBox = tk.Checkbutton(mainFrame, text="Romance", variable=romanceCheck, font=("Ubuntu Regular", 12), bg=bgColor, fg=txtColor, borderwidth=0, highlightthickness=0)
    romanceBox.pack(pady=10)
    thrillerBox = tk.Checkbutton(mainFrame, text="Thriller", variable=thrillerCheck, font=("Ubuntu Regular", 12), bg=bgColor, fg=txtColor, borderwidth=0, highlightthickness=0)
    thrillerBox.pack(pady=10)
    
    mainFrame.update_idletasks()

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
    canvas.pack(side="top", fill="both", expand=True, pady=10, padx=10)

    resultsFrame = tk.Frame(canvas, bg=bgColor)
    resultsFrame.pack(fill="both")

    scrollbar = tk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.create_window((0,0), window=resultsFrame, anchor="nw")
    resultsFrame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

    counter = 0
    buttonList = []

    for i in range(len(results)):
        # Load the poster
        poster = Image.open(f"img/posters/{results[i][0]}.jpg").resize((80,100))
        poster = ImageTk.PhotoImage(poster)
        images.append(poster)

        tempDate = results[i][2].split("-")[0]
        tempString = f"{results[i][1]} ({tempDate})"
        tempButton = tk.Button(resultsFrame, image=poster, command=lambda i=i: showMovie(window, results[i])).grid(row=counter, column=0)
        buttonList.append(tempButton)
        tk.Label(resultsFrame, text=tempString, font=("Ubuntu Regular", 12), bg=bgColor, fg=txtColor).grid(row=counter, column=1)
        
        counter += 1
        
    # Center the label and buttons
    mainFrame.update_idletasks()
    
    # Run the main loop
    window.mainloop()

    return window

    
# Show Movie function
def showMovie(window, movie):
    print("Show Movie")
    print(movie)

# Handle the results of the prediction using thresholds
def handleResults(results):
    # Map the results to the genre list
    res = {}
    counter = 0
    for key in genreList:
        res[key] = results[0][counter]
        counter += 1

    # sort the results
    sortedResults = sorted(res.items(), key=lambda x: x[1], reverse=True)

    # Get the top 3 genres that have a value greater than 0.5
    topGenres = []
    for genre in sortedResults:
        if genre[1] > 0.5:
            topGenres.append(genre)
        if len(topGenres) == 3:
            return topGenres
    
    # if not empty, return the top genres
    if len(topGenres) > 0:
        return topGenres
    
    # If there are less than 3 genres with a value greater than 0.5, get the top 3 genres until 0.42
    if len(topGenres) < 3:
        for genre in sortedResults:
            if genre[1] > 0.42:
                topGenres.append(genre)
            if len(topGenres) == 3:
                return topGenres
            
    # if not empty, return the top genres
    if len(topGenres) > 0:
        return topGenres

    # If there are still less than 3 genres, get the top 3 genres until 0.2
    if len(topGenres) < 3:
        for genre in sortedResults:
            if genre[1] > 0.2:
                topGenres.append(genre)
            if len(topGenres) == 3:
                return topGenres

    # if not empty, return the top genres
    if len(topGenres) > 0:
        return topGenres
    else:
        # If there are still less than 3 genres, get the top genre
        topGenres.append(sortedResults[0])

    return topGenres

# Find similar movies function
def findSimilarMovies(window, results):
    print("Genres predicted w threshold:", results)
    print("Find Similar Movies")
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Search for random movies containing the genres in the results, limit to 20
    genreString = ""
    for genre in results:
        genreString += f"genre LIKE '%{genre[0]}%' AND "
    genreString = genreString[:-5]

    print(genreString)

    c.execute(f"SELECT * FROM films WHERE {genreString} ORDER BY RANDOM() LIMIT 20")

    # Get the results of the search in paginated form
    results = c.fetchall()

    # Call the searchResults function
    searchResults(window, results)

    # Close the connection
    conn.close()


# Show Movie function
def showPredictedMovie(window, results, filename):
    print("Show Predicted Movie")
    # create a canvas to display the results
    # Create the main frame
    mainFrame = tk.Frame(window, width=720, height=640, bg=bgColor)
    mainFrame.grid(row=0, column=0)
    mainFrame.pack_propagate(False)

    # Create a button for each result with the poster and title
    images = []

    # Create a canvas to display the image and the genre labels beside it, place canvas under the sub label
    canvas = tk.Canvas(mainFrame, bg=bgColor)
    canvas.pack(pady=10)


    # Insert image into the canvas
    poster = Image.open(filename)
    poster = poster.resize((250, 375), Image.ANTIALIAS)
    poster = ImageTk.PhotoImage(poster)
    images.append(poster)

    # Handle the results of the prediction
    results = handleResults(results)

    tk.Label(canvas, image=poster).grid(row=0, column=0)

    # Create the genre labels
    for i in range(len(results)):
        tempString = f"{results[i][0]}: {results[i][1]:.3f}"
        tk.Label(canvas, text=tempString, font=("Ubuntu Regular", 12), bg=bgColor, fg=txtColor).grid(row=i+1, column=0)

    # Center the label and buttons
    mainFrame.update_idletasks()

    # Create the find similar movies button
    findButton = tk.Button(mainFrame, text="Find Similar Movies", font=("Ubuntu Regular", 12), bg=bgColor, fg=txtColor, highlightthickness = 0)
    findButton.pack(pady=20)

    # Find similar movies button command
    findButton.config(command=lambda: findSimilarMovies(window, results))

    # Run the main loop
    window.mainloop()

# Upload Poster function
def uploadPoster(window):
    print("Upload Poster")
    filename = filedialog.askopenfilename()
    print(f"Selected file: {filename}")

    # Open the image
    if sys.argv[1] == "vgg16":
        image = tf.keras.preprocessing.image.load_img(filename, target_size=(224, 224))
        image = tf.keras.preprocessing.image.img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image = tf.keras.applications.vgg16.preprocess_input(image)
    else:
        image = tf.keras.preprocessing.image.load_img(filename, target_size=(299, 299))
        image = tf.keras.preprocessing.image.img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image = tf.keras.applications.xception.preprocess_input(image)
    
    # predict the genre of the movie using the model
    results = model.predict(image)

    # Show the results of the prediction
    print("Results of the prediction")
    for i in range(len(results[0])):
        print(f"{genreList[i]}: {results[0][i]}")

    # Call the showPredictedMovie function
    showPredictedMovie(window, results, filename)

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
    
