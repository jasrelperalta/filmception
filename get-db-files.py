# This file is responsible for getting the necessary information about the films to be included in the database
# Through the use of TMDB API, we can get the necessary information about the films from the list in the CSV file

# Import the necessary libraries
import requests
import csv
import os
import json


from dotenv import load_dotenv

# Initialize the environment variables and other necessary configurations
load_dotenv("secret.env")

csv_file = "movie_dataset_combined2.csv"

if not os.path.exists(csv_file):
    print("CSV File does not exist")
    exit()

# tmdb api auth
def authenticate():
    url = "https://api.themoviedb.org/3/authentication"

    headers = {"accept": "application/json",
            "Authorization": f"Bearer {os.getenv('TMDB_API_READ')}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Authentication successful")
    else:
        print("Authentication failed")
        print(response.json().get("status_message"))


# tmdb api session
def create_session():
    url = "https://api.themoviedb.org/3/authentication/token/new"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {os.getenv('TMDB_API_READ')}"
    }

    response = requests.get(url, headers=headers)

    print(response.text)

    if response.status_code == 200:
        print("Session created")
        return response.json().get("request_token")
    else:
        print("Session creation failed")
        print(response.json().get("status_message"))

# append the necessary data in an input file
def store_data(data):
    with open("films.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow([data.get("id"), data.get("title"), data.get("release_date"), data.get("director"), data.get("overview"), data.get("poster_path"), data.get("genres")])

# loop to look for the films in the CSV file, to be get the necessary information about the films using the API
def get_db_files():
    with open(csv_file, "r") as file:
        reader = csv.reader(file)
        len_reader = len(list(reader))
        file.seek(0)
        next(reader)

        counter = 0
        for row in reader:
            # get the film id
            film_id = row[0]

            url = f"https://api.themoviedb.org/3/movie/{film_id}"

            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {os.getenv('TMDB_API_READ')}"
            }

            response = requests.get(url, headers=headers)
            print(f"[{counter}/{len_reader}]Getting data for {row}")

            # store the data in the database
            if response.status_code == 200:
                data = response.json()
                store_data(data)
                counter += 1
            else:
                print("Failed to get data")
                print(response.json().get("status_message"))

# main function
if __name__ == "__main__":
    authenticate()
    create_session()
    get_db_files()
