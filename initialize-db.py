# This file iitializes the database for the desktop application

import sqlite3
import csv

# CONSTANTS
DB_NAME = "filmception.db"

# CSV File


# Create the database
def createDB():
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Create the tables
    c.execute("CREATE TABLE films (id INTEGER PRIMARY KEY, title TEXT, year TEXT, synopsis TEXT, poster TEXT, genre TEXT)")

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

# populate the database
def populateDB():
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Open the CSV file
    with open("films.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)

        counter = 0
        len_reader = len(list(reader))
        file.seek(0)

        # Insert the data into the database
        for row in reader:
            print(f"[{counter+1}/{len_reader}]Current row: {row[1]}")
            # Example line: 
            # 940721,Godzilla Minus One,2023-11-03,"Postwar Japan is at its lowest point when a new crisis emerges in the form of a giant monster, baptized in the horrific power of the atomic bomb.",/hkxxMIGaiCTmrEArK7J56JTKUlB.jpg,"[{'id': 878, 'name': 'Science Fiction'}, {'id': 27, 'name': 'Horror'}, {'id': 28, 'name': 'Action'}]"
            c.execute("INSERT INTO films (id, title, year, synopsis, poster, genre) VALUES (?, ?, ?, ?, ?, ?)", (row[0], row[1], row[2], row[4], row[5], row[6]))
            counter += 1

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

# Initialize the database

if __name__ == "__main__":
    createDB()
    populateDB()
    print("Database initialized successfully!")
