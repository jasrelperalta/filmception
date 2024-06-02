# update genre from films.csv

import os
import csv


genreList = ["Action", "Adventure", "Animation", "Comedy", "Crime", "Drama", "Fantasy", "Romance", "Thriller"]

# Update the genres in the CSV file

with open("films.csv", "r") as file:
    reader = csv.reader(file)

    with open("films_updated.csv", "a") as writefile:
        writer = csv.writer(writefile)
        
        for row in reader:
            res = []
            print(type(row[-1]))
            temp = row[-1].strip("[]").split("}, {")
            
            for i in range(len(temp)):
                temp[i] = temp[i].strip("{}").split(", ")
                temp[i] = [x.split(": ")[1].strip("'") for x in temp[i]]
                print(temp[i])
                if temp[i][1] in genreList:
                    res.append(temp[i][1])
                if temp[i][1] == "Science Fiction":
                    res.append("Fantasy")
                if temp[i][1] == "Horror":
                    res.append("Thriller")
                if temp[i][1] == "Mystery":
                    res.append("Thriller")
                if temp[i][1] == "War":
                    res.append("Action")
                if temp[i][1] == "Western":
                    res.append("Action")
                if temp[i][1] == "Music":
                    res.append("Drama")
                if temp[i][1] == "Family":
                    res.append("Drama")

            row[-1] = res
            writer.writerow(row)
