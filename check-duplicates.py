# check if there is duplicate data in films.csv

import csv
import os
import json

with open("films.csv", "r") as file:
    reader = csv.reader(file)
    data = list(reader)

    for row in data:
        print(row)

    print("Data read successfully")
    print("Checking for duplicates")

    # check for duplicates
    for i in range(len(data)):
        for j in range(i+1, len(data)):
            if data[i] == data[j]:
                print(f"Duplicate found at {i+1} and {j+1}")
                print(data[i])
                print(data[j])