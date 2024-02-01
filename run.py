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
        for task in list(todo_list):
            # after escape character 033[1m sets text weight to bold,
            # 033[0m after task resets to default
            print(f'\033[1m {task} \033[m')


def create_task():
    """
    Asks user to input their task and appends it to Tasks worksheet
    """
    task = input('\nEnter your todo: ')
    # Assigning tasks worksheet to task_sheet variable
    task_list = SHEET.worksheet('Tasks')
    # Appending the task to the worksheet row
    task_list.append_row([task])
    print('\nAdding your new task...')
    # Showing the updated list to the user
    display_list()


def task_done():
    """
    Use gspread .find method to match user input to cell, then move to Done tab
    """
    # Refactor? Move list to global scope with list in create_task function?
    task_list = SHEET.worksheet('Tasks')
    # Assigning Done worksheet to done_list var
    done_list = SHEET.worksheet('Done')
    # Shows users tasks on their list
    display_list()
    # Asks user which task they have completed
    # This gets assigned to find_task
    find_task = input("Which task have you completed? ")

    try:
        # Looks for cell with matching value to find_task,
        # Assign this to the done_task var
        done_task = task_list.find(find_task)
        # Adds the completed task to the Done sheet
        done_list.append_row([done_task.value])
        # Need to delete task from cell and shift all cells up one here...

    # If no matching task is found, user given choice to try again or return to menu
    except (TypeError, AttributeError) as e:
        print(f'''\nNo task found matching {find_task}... Please try again, \
or enter the word menu to return to the main menu.\n''')
        # Convert string to lower in case caps lock is enabled
        if find_task.lower() == 'menu':
            # Return user to the menu
            user_options()
        else:
            # Continue to the task_done function again
            task_done()


def user_options():
    """
    Uses if/else to take user input and run corresponding function
    """

    choice = input('''\nWhat would you like to do?\n
1: Create a new task\n2: View your to do list
3: Mark a task as done
4: Edit a task\nOr type 'exit' to quit: ''')
    # Checking user input against the listed options
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
        task_done()
        user_options()
    elif choice == str(4):
        print("")
        print('I need to make function to edit task...')
        user_options()
    elif choice.lower() == 'exit':
        exit()
    # Tell user if their choice is not valid
    # and runs the options menu again
    else:
        print('\nInvalid selection, please try again.\n')
        user_options()


def main():
    app_load()


main()
