# check all the genres in the database and check if there are any duplicates

import os
import csv

genreList = ["Action", "Adventure", "Animation", "Comedy", "Crime", "Drama", "Fantasy", "Romance", "Thriller"]

# Update the genres in the CSV file

with open("films.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        genreSet = set()
        print(row[-1])
        temp = row[-1].strip("[]").split("', '")
        print(temp)
        temp = [x.strip("'") for x in temp]
        print(temp)
        for genre in temp:
            genreSet.add(genre)
        # Edit row[-1] to be a list of genres
        row[-1] = list(genreSet)
        print(row[-1])
        print(row)
        # Update the whole row in the CSV file
        with open("films_updated.csv", "a") as writefile:
            writer = csv.writer(writefile)
            writer.writerow(row)