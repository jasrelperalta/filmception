# update genre from films.csv
import os
import csv

with open("films_updated.csv", "r") as file:
    reader = csv.reader(file)

    for row in reader:
        print(row[2])
        row[2] = int(row[2].split("-")[0])
        print(row)
        break