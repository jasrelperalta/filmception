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
    c.execute("""CREATE TABLE IF NOT EXISTS films (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        year INTEGER NOT NULL,
        director TEXT NOT NULL,
        synopsis TEXT NOT NULL,
        poster TEXT NOT NULL,
        genre TEXT NOT NULL,
    )""")

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

if __name__ == "__main__":
    createDB()

# populate the database
def populateDB():
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Open the CSV file
    with open("films.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)

        # Insert the data into the database
        for row in reader:
            c.execute("INSERT INTO films (title, year, director, synopsis, poster, genre) VALUES (?, ?, ?, ?, ?, ?)", row)

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()