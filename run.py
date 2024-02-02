import gspread
from google.oauth2.service_account import Credentials
import os

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('todo-list-app')


def clear_terminal():
    """
    Clears the terminal when called, improving readability
    """
    os.system('clear')


def app_load():
    """
    Prints welcome message to user on app load and runs user_options function
    """
    clear_terminal()
    print('\nWelcome to your to-do list')
    user_options()


def display_list():
    """
    Checks if To Do list is empty, if so, asks user to add a task
    if not empty, prints tasks
    """
    print('Loading your to-do list...')
    clear_terminal()
    todo_list = SHEET.worksheet('Tasks').get_all_values()
    if todo_list == []:
        print('Your To Do list is empty! Add a task.')
        create_task()
    else:
        print('Here are your tasks to complete:')
        for task in list(todo_list):
            # after escape character 033[1m sets text weight to bold,
            # 033[0m after task resets to default
            print(f'\033[1m {task} \033[m')


def display_done_tasks():
    """
    Displays tasks on the done worksheet
    """
    print('Loading your completed tasks...')
    # Clearing terminal
    clear_terminal()
    # Assigning values to done_list to print to terminal
    done_list = SHEET.worksheet('Done').get_all_values()
    # Assigning worksheet to done_sheet for gspread .clear() function
    done_sheet = SHEET.worksheet('Done')
    # Prints message and loads main menu if no tasks are completed
    if done_list == []:
        print('You have no completed tasks!\n')
        print('Loading main menu...\n')
        user_options()
    # Prints # of tasks in Done sheet and lists them in bold
    else:
        print(f"""Well done! You've completed {len(done_list)} tasks.
Here's your full list: """)
        for task in list(done_list):
            print(f'\033[1m {task} \033[m')
        # Gets user choice of what to do next
        choice = input('''Enter MENU to return to the \
main menu, CLEAR to clear your Completed tasks list, or QUIT to exit the app: ''')
        # Reloads main menu
        if choice.lower() == 'menu':
            clear_terminal()
            user_options()
        # Clears 'Done' worksheet
        elif choice.lower() == 'clear':
            # Set condition to True for while loop
            deleting = True
            while deleting is True:
                print(f"You are about to delete your completed tasks")
                print("Are you sure?")
                print("")
                # Confirming user's choice
                confirm_deletion = input("Type YES to confirm,\
 or NO to return to main menu (input is case-sensitive): ")
                # Deleting all data from sheet if YES
                if confirm_deletion == 'YES':
                    print(f"Deleting your completed tasks...")
                    done_sheet.clear()
                    # Breaks while loop and returns to menu
                    deleting = False
                    clear_terminal()
                    user_options()
                # Breaks while loop and returns to
                # menu with no data deleted if NO
                elif confirm_deletion == 'NO':
                    deleting = False
                    clear_terminal()
                    user_options()
                # While loop remains True and user
                # asked to try again if anything else entered
                else:
                    print('Invalid choice, please try again')
        # Program exit if user chooses 'quit'
        elif choice.lower() == 'quit':
            exit()
        else:
            print('Invalid selection. Please try again: ')


def create_task():
    """
    Asks user to input their task and appends it to Tasks worksheet
    """
    print('Loading create task function...')
    clear_terminal()
    task = input('\nEnter your todo: ')
    # Assigning tasks worksheet to task_sheet variable
    task_list = SHEET.worksheet('Tasks')
    # Appending the task to the worksheet row
    task_list.append_row([task])
    print('\nAdding your new task...')
    # Showing the updated list to the user
    display_list()


def delete_task():
    """
    Use gspread .find method to match user input to cell, then delete row
    """
    clear_terminal()
    # Assigning Tasks worksheet to variable
    task_list = SHEET.worksheet('Tasks')
    # Displaying To Do list to user
    display_list()
    # Adding user's task to delete to find_task variable
    find_task = input('Which task would you like to delete? ')
    try:
        # Finding task and assigning to var
        task_to_delete = task_list.find(find_task)
        # Sets True condition for deletion while loop
        deleting = True
        # Keeps deletion in process until valid input has been confirmed
        # or stopped by the user, will repeat if invalid data entered
        while deleting is True:
            print(f"You are about to delete {task_to_delete}")
            print("Are you sure?")
            print("")
            # Confirming user's choice
            confirm_deletion = input("Type YES to confirm,\
 or NO to return to menu (input is case-sensitive): ")
            # Deleting task row if YES
            if confirm_deletion == 'YES':
                print(f"Deleting {[task_to_delete]}...")
                task_list.delete_rows(task_to_delete.row)
                # Breaks while loop and returns to menu
                deleting = False
                clear_terminal()
                user_options()
            # Breaks while loop and returns to menu with no data deleted if NO
            elif confirm_deletion == 'NO':
                deleting = False
                clear_terminal()
                user_options()
            # While loop remains True and user asked to try again
            else:
                print('Invalid choice, please try again')
    # except statement will handle error if task matching input not found
    except (TypeError, AttributeError) as e:
        print(f'''\nNo task found matching {find_task}... Please try again, \
or enter MENU to return to the main menu.\n''')
        # Convert string to lower in case caps lock is enabled
        if find_task.lower() == 'menu':
            # Return user to the menu
            user_options()
        else:
            # Continue to the delete_task function again
            delete_task()


def task_done():
    """
    Use gspread .find method to match user input to cell, then move to Done tab
    """
    clear_terminal()
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
        # Deletes task from Task sheet
        task_list.delete_rows(done_task.row)
        # Adds the completed task to the Done sheet
        done_list.append_row([done_task.value])

    # If no matching task is found, user given choice
    # to try again or return to menu
    except (TypeError, AttributeError) as e:
        print(f'''\nNo task found matching {find_task}... Please try again, \
or enter MENU to return to the main menu.\n''')
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
1: Create a new task\n2: View your To Do list
3: Mark a task as done
4: Delete a task from your To Do list\n5: View your completed tasks
Or type 'exit' to quit: ''')
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
        delete_task()
    elif choice == str(5):
        print('Loading your completed tasks...')
        display_done_tasks()
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
