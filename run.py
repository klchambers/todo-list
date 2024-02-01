import gspread
from google.oauth2.service_account import Credentials

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
    print('Welcome to your to-do list')
    print("")
    display_list()


def display_list():
    todo_list = SHEET.worksheet('Tasks').get_all_values()
    if todo_list == []:
        print('Your to do list is empty! Add a task.')
        create_task()
    else:
        print('Here are your tasks to complete:')
        print(todo_list)


def create_task():
    task = input('\nEnter your todo: ')
    list = SHEET.worksheet('Tasks')
    list.append_row([task])
    print("")
    display_list()


def main():
    app_load()


main()
#create_task()