import gspread
from google.oauth2.service_account import Credentials
import os  # use os.system('clear') to clean up output

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('todo-list-app')


def app_load():
    """
    Prints welcome message to user on app load and runs user_options function
    """
    print('\nWelcome to your to-do list')
    user_options()


def display_list():
    """
    Checks if to do list is empty, if so, asks user to add a task
    if not empty, prints tasks
    """
    todo_list = SHEET.worksheet('Tasks').get_all_values()
    if todo_list == []:
        print('Your to do list is empty! Add a task.')
        create_task()
    else:
        print('Here are your tasks to complete:')
        print(todo_list)


def create_task():
    """
    Asks user to input their task and appends it to Tasks worksheet
    """
    task = input('\nEnter your todo: ')
    list = SHEET.worksheet('Tasks')
    list.append_row([task])
    print("")
    display_list()


def user_options():
    """
    Uses if/else to take user input and run corresponding function
    """

    choice = input('''\nWhat would you like to do?\n
1: Create a new task\n2: View your to do list
3: Edit a task\nType 'exit' to quit: ''')

    if choice == str(1):
        print("")
        create_task()
        user_options()
    elif choice == str(2):
        print("")
        display_list()
        user_options()
    elif choice == str(3):
        print("")
        print('I need to make function to edit task...')
        user_options()
    elif choice.lower() == 'exit':
        exit()
    else:
        print('\nInvalid selection, please try again.\n')
        user_options()


def main():
    app_load()


main()
