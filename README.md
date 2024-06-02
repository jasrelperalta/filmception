# FilmCeption

## Description

FilmCeption is a desktop application that allows users to multilabel classify movie posters, and also lets the users find all the similarly labeled films to the poster. The application makes use of a pre-trained Xception model to classify movie posters into 9 different genres. The genres are: Action, Adventure, Animation, Comedy, Crime, Drama, Fantasy, Romance, and Thriller. The application also provides a brief description of the movie and its release date. The desktop application is built using Python and the Tkinter library, and sqlite for the database.

## Usage

To use the application, get the necessary files for the database first. NOTE: The database files are not included in the repository. To get the database files, run the following command ONCE (no need to run this command every time you run the application):

```bash
python3 get_db-files.py
```

Then run the main application.

```bash
python3 main.py
```

## Dependencies

- tkinter
- pyglet
- 

## Author

- Jasrel Peralta
