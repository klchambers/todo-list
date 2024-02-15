import gspread
from google.oauth2.service_account import Credentials
import os
from datetime import datetime
import csv
import pyperclip

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
    # if else statement to clear terminal depending on operating system
    # was posted by user 'poke' on Stack Overflow on Jan 18, 2010
    # if operating system is Windows, use 'cls', or clear if unix
    os.system('cls' if os.name == 'nt' else 'clear')


def app_load():
    """
    Clears screen & prints welcome message to user on app load
    before running user_options function
    """
    clear_terminal()
    # ASCII art generated using Peter Gillespie's text to ASCII art generator
    # Available at https://patorjk.com/software/taag
    print(r"""
 _____      ______        _     _     _   _
|_   _|     |  _  \      | |   (_)   | | | |
  | | ___   | | | |___   | |    _ ___| |_| |
  | |/ _ \  | | | / _ \  | |   | / __| __| |
  | | (_) | | |/ / (_) | | |___| \__ \ |_|_|
  \_/\___/  |___/ \___/  \_____/_|___/\__(_)
""")
    # Printing options menu to user
    user_options()


def display_list():
    """
    Checks if To Do list is empty, if so, asks user to add a task
    if not empty, prints tasks
    """

    # Assigning tasks worksheet to todo_list variable
    todo_list = SHEET.worksheet('Tasks').get_all_values()
    # Checking if Tasks list has to do items
    if len(todo_list) <= 1:
        choice = input("""\nYour To Do list is empty! \
Would you like to add a task?\nEnter YES to create a task,\
 or press any key to return to menu: """)
        # Clearing terminal and running create_task function
        if choice.lower() == 'yes':
            clear_terminal()
            create_task()
        # Clearing terminal and taking user to options menu
        else:
            clear_terminal()
            user_options()
    else:
        # For loop starts at index 1 to avoid printing header row
        for index, task in enumerate(todo_list[1:], 1):
            # after escape character 033[1m sets text weight to bold,
            # 033[0m after task resets to default
            # [0] index ensures that task value is printed rather than object
            # Code adapted from examples posted by Peter Mortensen and Bacara
            # On Stack Overflow
            print(f'{index}\033[1m {task[0]} (created on {task[1]})\033[m')


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
    if len(done_list) <= 1:
        print('You have no completed tasks!\n')
        input('Press the Enter key to return to the main menu')
        app_load()
    # Prints # of tasks in Done sheet and lists them in bold
    else:
        print(f"""Well done! You've completed {len(done_list)} tasks.
Here's your full list: """)
        for task in list(done_list[1:]):
            # after escape character 033[1m sets text weight to bold,
            # 033[0m after task resets to default
            # [0] index ensures that task value is printed rather than object
            # Code adapted from examples posted by Peter Mortensen and Bacara
            # On Stack Overflow
            print(f'\033[1m • {task[0]} (completed on {task[1]}) \033[m')
        # Gets user choice of what to do next
        choice = input('''Enter 'menu' to return to the main menu,
'clear' to clear your Completed tasks list,
or 'quit' to exit the app: ''')
        # Reloads main menu
        if choice.lower() == 'menu':
            clear_terminal()
            user_options()
        # Clears 'Done' worksheet
        elif choice.lower() == 'clear':
            # Set condition to True for while loop
            deleting = True
            while deleting is True:
                print("You are about to delete your completed tasks")
                print("Are you sure?")
                print("")
                # Confirming user's choice
                confirm_deletion = input("Type YES to confirm,\
 or NO to return to main menu (input is case-sensitive): ")
                # Deleting all data from sheet if YES
                if confirm_deletion == 'YES':
                    print("Deleting your completed tasks...")
                    done_sheet.delete_rows(2, len(done_list))
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
            clear_terminal()
            exit()
        else:
            input('Invalid selection. Press any key to continue: ')
            display_done_tasks()


def create_task():
    """
    Asks user to input their task and appends it to Tasks worksheet
    """
    print('Loading create task function...')
    clear_terminal()
    # Assigns the current date to date_created variable
    # Date formatting using. strftime() adapted from example posted by
    # NPE on Stack Overflow
    date_created = datetime.today().strftime('%b %d, %Y')
    # Assigning user input to task variable, to be appended to Task sheet
    task = input('Enter your new task: ')
    # Declaring a list of critical keywords that shouldn't be entered
    # as task names
    important_keywords = ['quit', 'menu', 'clear', 'yes', 'no']
    if any(keyword in task.strip().lower() for keyword in important_keywords):
        print(f'You cannot create a task called {task}...')
        input("Press enter to try again.")
        create_task()
    # Assigning tasks worksheet to task_sheet variable
    task_list = SHEET.worksheet('Tasks')
    # Appending the task to the worksheet row
    task_list.append_row([task, str(date_created)])
    # Visual feedback confirming to the user that their action is in progress
    print('\nAdding your new task...')
    # Showing the updated list to the user
    user_options()


def delete_task():
    """
    Use gspread .find method to match user input to cell, then delete row
    """
    # Assigning Tasks worksheet to variable
    task_list = SHEET.worksheet('Tasks')
    # Displaying To Do list to user
    display_list()
    # Adding user's task to delete to find_task variable
    find_task = input("""Which task would you like to delete?
Alternatively, Enter 'MENU' to return to options menu: """)
    # Checking if input is equal to 'menu'
    # .lower() used in case user capitalises any letter
    if find_task.lower() == 'menu':
        app_load()
    try:
        # Assign find_task to task_index if an int, minus one to account
        # for zero index
        task_index = int(find_task)-1
        print(f'You are about to delete the task: {find_task}.')
        print('Are you sure?')
        print("")
        confirm_deletion = input("""Type YES to confirm,\
 or NO to return to menu (input is case-sensitive) """)
        if confirm_deletion == "YES":
            # Adding 1 to target correct row, and to prevent deleting row 0
            task_list.delete_rows(task_index + 2)
            app_load()
        else:
            app_load()
    except ValueError:
        try:
            # Finding task and assigning to var
            task_to_delete = task_list.find(find_task)
            # Sets True condition for deletion while loop
            deleting = True
            # Keeps deletion in process until valid input has been confirmed
            # or stopped by the user, will repeat if invalid data entered
            while deleting is True:
                print(f"You are about to delete the task: \
    '{task_to_delete.value}'")
                print("Are you sure?")
                print("")
                # Confirming user's choice
                confirm_deletion = input("Type YES to confirm,\
    or NO to return to menu (input is case-sensitive): ")
                # Deleting task row if YES
                if confirm_deletion == 'YES':
                    print(f"Deleting {task_to_delete.value}...")
                    task_list.delete_rows(task_to_delete.row)
                    # Breaks while loop and returns to menu
                    deleting = False
                    app_load()
                # Breaks while loop and returns to menu
                # with no data deleted if NO
                elif confirm_deletion == 'NO':
                    deleting = False
                    # clear_terminal()
                    app_load()
                # While loop remains True and user asked to try again
                else:
                    print('Invalid choice, please try again')
        # except statement will handle error if task matching input not found
        except (TypeError, AttributeError):
            print(f'''\nNo task found matching\
    '{find_task}'... Please try again.\n''')
            # Continue to the delete_task function again
            delete_task()


def task_done():
    """
    Use gspread .find method to match user input to cell, then move to Done tab
    """
    # clear_terminal()
    task_list = SHEET.worksheet('Tasks')
    # Assigning Done worksheet to done_list var
    done_list = SHEET.worksheet('Done')
    # Assigning completed date to be appended to second column
    date_completed = datetime.today().strftime('%b %d, %Y')
    # Shows users tasks on their list
    display_list()
    # Asks user which task they have completed
    # This gets assigned to find_task
    find_task = input("""\nWhich task have you completed?
Enter the task index number or task title.
Alternatively, Enter 'MENU' to return to options menu: """)
    if find_task == 'menu':
        app_load()
    try:
        # Assign find_task to task_index if an int, minus one to account
        # for zero index
        task_index = int(find_task)-1
        done_task = task_list.cell(task_index + 2, 1).value
        # Adding 1 to target correct row, and to prevent deleting row 0
        task_list.delete_rows(task_index + 2)
        # Appending done_task to the Done worksheet, with date completed
        done_list.append_row([done_task, str(date_completed)])
        app_load()
    except ValueError:
        try:
            # Looks for cell with matching value to find_task,
            # Assign this to the done_task var
            done_task = task_list.find(find_task)
            # Deletes task from Task sheet
            task_list.delete_rows(done_task.row)
            # Adds the completed task to the Done sheet
            done_list.append_row([done_task.value, str(date_completed)])
            # Clears terminal and reloads app menu display
            clear_terminal()
            app_load()

        # If no matching task is found, user given choice
        # to try again or return to menu
        except (TypeError, AttributeError):
            print(f'\nNo task found matching {find_task}... \
Please try again.\n')
            # Convert string to lower in case caps lock is enabled
            task_done()


def export_data():
    """
    writes data in Tasks worksheet to CSV format and saves in directory
    """
    try:
        # Assigns string to be saved to the file name
        # datetime.now() gets current date and time to create unique file names
        file_name = f'tasks_list_{datetime.now()}.csv'
        # os.path.expand user adapted from code posted to
        # Stack Overflow by users theDude and nagyl
        downloads_path = os.path.expanduser('~/Downloads')
        file_to_export = os.path.join(downloads_path, file_name)

        # Adapted from code posted to ioflood.com/blog by
        # Gabriel Ramuglia 13/9/23
        with open(file_to_export, 'w', newline='') as file:
            # Getting valies from Tasks worksheet
            todo_list = SHEET.worksheet('Tasks').get_all_values()
            #
            done_list = SHEET.worksheet('Done').get_all_values()

            all_data = SHEET.worksheets()
            # Assigning headers to field_headers variable to
            # print on first line

            writer = csv.writer(file)
            writer.writerow(['To Do List:'])

            # for loop iterates over values on sheet, writes them to CSV file
            for value in todo_list:
                writer.writerow(value)
            writer.writerow(['Completed Tasks:'])

            for value in done_list:
                writer.writerow(value)
        print(f'CSV file generated: {file_name}')
        print(f'''You can find the file in the Downloads folder: \
{downloads_path}''')
        input('Press the enter key to return to the main menu')
        clear_terminal()
        user_options()
    except FileNotFoundError as e:
        all_data = SHEET.worksheets()
        print(f'\nError exporting CSV file: {e}\n')
        print('Downloading csv files is not available via Heroku deployment.')
        choice = input('''Would you like to copy your csv data to the \
clipboard?\n
Enter YES to copy csv data, or NO to return to the main menu.
(input is case-sensitive) ''')
        if choice == 'YES':
            data_to_copy = ''
            for worksheet in all_data:
                # Extract data from each worksheet
                data = worksheet.get_all_values()
                # Convert data to string and concatenate
                data_to_copy += str(data) + ', ' + '\n\n'
            pyperclip.copy(data_to_copy)
            input('''Data successfully copied to clipboard!\n
    Press the Enter key to return to the main menu''')
        elif choice == 'NO':
            clear_terminal()
            app_load()
        else:
            print('Invalid input. Please try again.')
            export_data()
    finally:
        try:
            # Get data from Google Sheets
            todo_list = SHEET.worksheet('Tasks').get_all_values()
            done_list = SHEET.worksheet('Done').get_all_values()

            print('Cannot copy data to clipboard in Herokud deployment.')
            print('Printing data in csv format for manual copy/paste...\n')
            # Print data in CSV format to terminal
            print('To Do List:')
            for row in todo_list:
                print(','.join(row))

            print('\nCompleted Tasks:')
            for row in done_list:
                print(','.join(row))

            input('\nPress the Enter key to return to the menu: ')
            app_load()
        except Exception as e:
            print(f'Error exporting Google Sheets data: {e}')
            input('\nPress the Enter key to return to the menu: ')
            app_load()


def user_options():
    """
    Uses if/else to take user input and run corresponding function
    """
    todo_list = SHEET.worksheet('Tasks').get_all_values()
    # Checking if Tasks list has to do items
    if len(todo_list) <= 1:
        # If empty, prints the following in bold
        print('\033[1mYour To Do list is empty!\033[0m')
    else:
        print('Here are your tasks to complete:')
        for task in list(todo_list[1:]):
            # after escape character 033[1m sets text weight to bold,
            # 033[0m after task resets to default
            # [0] index ensures that task value is printed rather than object
            # Code adapted from examples posted by Peter Mortensen and Bacara
            # On Stack Overflow
            print(f'\033[1m • {task[0]} (created on {task[1]})\033[m')
    choice = input('''\nWhat would you like to do?\n
1: Create a new task\n2: Mark a task as done
3: Delete a task from your To Do list\n4: View your completed tasks
5: Export your tasks list to CSV\nOr type 'exit' to quit: ''')
    # Checking user input against the listed options
    if choice == str(1):
        print("")
        create_task()
        app_load()
    elif choice == str(2):
        print("")
        task_done()
    elif choice == str(3):
        print("")
        delete_task()
    elif choice == str(4):
        print("")
        display_done_tasks()
    elif choice == str(5):
        print("")
        export_data()
    elif choice.lower() == 'exit':
        clear_terminal()
        exit()
    # Tell user if their choice is not valid
    # and runs the options menu again
    else:
        print('\nInvalid selection.\n')
        input('Press Enter to continue')
        app_load()


def main():
    app_load()


main()
