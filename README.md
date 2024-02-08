![To Do List app ASCII art](documentation/toDoListASCIIArt.png)

**Table of contents:**

- [Introduction](#introduction)
- [Deployed Site](#deployed-site)
- [User Experience](#user-experience)
  - [User Goals](#user-goals)
  - [User Stories](#user-stories)
  - [Site Owner's Goals](#site-owners-goals)
- [Features](#features)
  - [Main Menu](#main-menu)
  - [Creating a Task](#creating-a-task)
  - [Marking Tasks as Done](#marking-tasks-as-done)
  - [Completed Tasks List](#completed-tasks-list)
  - [Data Model](#data-model)
- [Testing and Validation](#testing-and-validation)
  - [Testing Methodology](#testing-methodology)
  - [Pep-8 Code Analysis](#pep-8-code-analysis)
  - [Development](#development)
  - [Contributing](#contributing)
  - [Deployment](#deployment)
  - [Further Development and Future Features](#further-development-and-future-features)
- [Technologies Used](#technologies-used)
- [Acknowledgements](#acknowledgements)

<a id=introduction></a>

## Introduction



<a id=deployed-site></a>

## Deployed Site

The program has been deployed to Heroku and can be accessed [here](https://pp3todoapp-ab2e466bceb0.herokuapp.com/).

<a id=user-experience></a>

## User Experience

<a id=user-goals></a>

### User Goals

- I would like to store To Do list data, check off tasks when I complete them, and view and delete a list of completed tasks
- I would like the app to record the date that I create and complete tasks, for later reference
- I would like the app to display my To Do list in a user-friendly, readable format
- I would like the data to be persistent, saving to a database so I can view it later, even after closing the program

<a id=user-stories></a>

### User Stories

- The app should be intuitive, and display actionable and informative data
- The app should be responsive to my input, and inform me if I make any mistakes or input any invalid data
- The app should store my data, and use persistent storage to allow me to view it at a later date after closing the app
- The app should clear the terminal display appropriately after certain actions, such as when I delete data, clear a list, or exit the program

<a id=site-owners-goals></a>

### Site Owner's Goals

- I aim to create a useful program through which data can be stored with relevant contextual information, such as dates and priorities/importance
- I aim to create a program which a user can quit, and come back to at a later date
- I aim to implement defensive design in the program, so that exceptions and errors are caught and handled well, with as little inconvenience to the user as possible

<a id=features></a>

## Features



<a id=main-menu></a>

### Main menu



<a id=creating-a-task></a>

### Creating a Task



<a id=marking-tasks-as-done></a>

### Marking Tasks as Done



<a id=completed-tasks-list></a>

### Completed Tasks List



<a id=data-model></a>

### Data Model



<a id=testing-and-validation></a>

## Testing and Validation



<a id=testing-methodology></a>

### Testing Methodology



<a id=pep8-code-analysis></a>

#### Pep-8 Code Analysis



<a id=development-and-deployment></a>

## Development and Deployment



<a id=development></a>

### Development



<a id=contributing></a>

### Contributing



<a id=deployment></a>

### Deployment



<a id=further-development-and-future-features></a>

### Further Development and Future Features



<a id=technologies-used></a>

## Technologies Used

- [Visual Studio Code](https://code.visualstudio.com/): Code editing
- [GitHub](https://github.com/): Source control
- [Heroku](https://www.heroku.com): Live deployment of site
- [Code Institute PEP8 Linter](https://pep8ci.herokuapp.com/): Python code analysis tool
- [datetime Python module](https://docs.python.org/3/library/datetime.html): used to input date data into spreadsheet
- [Google Sheets](https://www.google.com/sheets/about/): Cloud-based spreadsheet editor used to store data
- [gspread API](https://docs.gspread.org/en/latest/): Python API for Google Sheets, used to access spreadsheets, provide access to run.py, and read, write and format cells
- [Google Drive API](https://developers.google.com/drive/api/guides/about-sdk): REST API, credentials, and authorisation

<a id=acknowledgements></a>

## Acknowledgements

Date formatting using `strftime()` method adapted from an example posted by [NPE](https://stackoverflow.com/users/367273/npe) in [this](https://stackoverflow.com/questions/6288892/python-how-to-convert-datetime-format) Stack Overflow thread.

ANSI character methods to print bold text in the terminal adapted from examples posted by [Peter Mortensen](https://stackoverflow.com/users/63550/peter-mortensen) and [Bacara](https://stackoverflow.com/users/1770999/bacara) in [this](https://stackoverflow.com/questions/8924173/how-can-i-print-bold-text-in-python#:~:text=In%20Python%2C%20escape%20sequences%20are,want%20to%20represent%20in%20bold.) Stack Overflow thread.

[This](https://patorjk.com/software/taag) text to ASCII art generator by Patrick Gillespie on [patrorjk.com](https://patorjk.com/) was used to generate the ASCII art displayed on app load.

Course content from Code Institute's Diploma in Full Stack Software Development has been useful and in teaching programming concepts and Python methods.

Guidance from Code Institute mentor Brian O'Hare has been invaluable throughout stages of this project's inception and development.
