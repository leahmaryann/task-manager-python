# ========== Task Manager System ==========
"""
This module functions as a task manager system.

Users are able to log-in, register, manage tasks and create reports.
Admin users have increased funcionality as they are able to manage users,
view statistics, and create task and user reports.
"""
# ========== Importing external modules ==========
from datetime import date
from datetime import datetime

# File was not being recognised
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ==== Login Section ====

# Create a dictionary that stores usernames and passwords
user_data = {}


def read_user_data():
    """
    This function opens the user.txt file and reads the data from
    this file.

    The usernames and passwords are stored in the user_data dictionary.

    """
    try:
        # Open the user file in read mode
        with open('user.txt', 'r', encoding='utf-8') as file:

            # Iterate through and read each line in the file
            for line in file:
                keys, values = line.strip().split(", ")
                user_data[keys] = values

        # print(user_data)
        return user_data

    except FileNotFoundError:
        print("The user.txt was not found")


def login():
    """
    The user is continuously asked to enter their username and password,
    until they enter valid credentials.
    """
    while True:
        # Request the username
        username = input("Please enter your username: \n").strip().lower()

        # Continue requesting username until the input is valid.
        if username not in user_data:
            print("Invalid username.\n")
            continue

        # If the username is valid, request the password.
        while True:
            password = input("Please enter your password: \n").strip()

            # Print an error message if the password is incorrect.
            if password != user_data[username]:
                print("Invalid password.\n")
                continue

            else:
                print("Login Successful\n")
                return username


def admin_menu(username):
    """
    Displays, loops and controls the function of the admin menu
    until the user exits.

    Parameters:
    username (str): The username of the user that is logged in. Makes sure
    that only the admin user has access to specific functionalities.
    """
    while True:

        # Continuously request the user to select a menu option until a valid
        # option is selected
        menu = input(
            "Select one of the following options:\n"
            "r - register a user\n"
            "a - add task\n"
            "va - view all tasks\n"
            "vm - view my tasks\n"
            "vc - view completed tasks\n"
            "del - delete tasks\n"
            "ds - display statistics\n"
            "gr - generate reports\n"
            "e - exit:\n"
        ).lower()

        # Register a new user
        if menu == 'r':
            reg_user(username)

        # Add a new task
        elif menu == 'a':
            add_task()

        # View all tasks
        elif menu == 'va':
            view_all()

        # View tasks assigned to the user logged in.
        elif menu == 'vm':
            view_mine(username)

        # View all completed tasks
        elif menu == 'vc':
            view_completed()

        # Display task and user statistics
        elif menu == 'ds':
            display_statistics()

        # Create task and user statistical overview reports
        elif menu == 'gr':
            generate_report()

        # Delete a task
        elif menu == 'del':
            delete_task()

        # Exit the system
        elif menu == 'e':
            print("Goodbye")
            exit()

        # Error message for invalid inputs
        else:
            print("You have entered an invalid input. Please try again")


def user_menu(username):
    """
    Displays, loops and controls the function of the user menu
    until the user exits.

    Parameters:
    username (str): The username of the user that is logged in. Makes sure
    that non-admin users have access to limited functionalities.
    """

    # Continuously request the user to select a menu option until a valid
    # option is selected.
    while True:
        menu = input(
            "Select one of the following options:\n"
            "a - add task\n"
            "va - view all tasks\n"
            "vm - view my tasks\n"
            "e - exit:\n"
        ).lower()

        # Add a new task
        if menu == 'a':
            add_task()

        # View all tasks
        elif menu == 'va':
            view_all()

        # View tasks assigned to the user logged in.
        elif menu == 'vm':
            view_mine(username)

        # Exit the system
        elif menu == 'e':
            print("Goodbye")
            exit()

        # Error message for invalid inputs
        else:
            print("You have entered an invalid input. Please try again")


def reg_user(username):
    """
    Admin users use this function to add new users to the system.

    Credentials of new users are validated and then saved to the 'user.txt'
    file. The read_user_data() function is then called to update the
    'user-data' dictionary.

    Parameters:
    username (str): The admin user must be logged in to access this function.
    """

    # Check if the admin user is logged in.
    if username != "admin":
        print("Only the admin user is allowed to register new users.")
        return      # Exit if the user is not admin.

    # Declare 'user_data' as global variable.
    global user_data

    # Open the 'user.txt' file and loop through each line.
    try:
        with open('user.txt', 'r', encoding='utf-8') as file:
            for line in file:

                # Split line into key(username) and value(password) pairs
                # and save in dictionary.
                keys, values = line.strip().split(", ")
                user_data[keys.lower()] = values

    # If the 'user.txt' file is not found, save an empty dictionary.
    except FileNotFoundError:
        user_data = {}

    while True:
        new_username = input("Please enter a username: \n").strip().lower()

        # Check if the input is blank.
        if not new_username:
            print("This field cannot be blank.")
            continue

        # Check if the username already exists.
        if new_username in user_data:
            print("This username already exists. Please try again.")
            continue

        # Check if the username only contains numbers.
        if new_username.isnumeric():
            print("The username cannot consist of only numbers")
            continue
        break       # Exit the loop

    while True:
        new_password = input("Please enter a password: \n").strip()

        # Check if the input is blank.
        if not new_password:
            print("This field cannot be blank")
            continue
        break       # Exit the loop

    while True:
        # Request the user to input the same password
        confirm_password = input("Please re-enter your password: \n").strip()

        # If passwords do not match, continue to loop, else exit the loop.
        if confirm_password != new_password:
            print("The passwords do not match")
            continue
        break

    # Write the new user credentials to the 'user.txt' file.
    with open("user.txt", "a", encoding='utf-8') as file:
        file.write(f"\n{new_username}, {new_password}")

    print("New user added")

    # Load the updated user information.
    user_data = read_user_data()


def add_task():
    """
    Allows users to create tasks and assign them to current users.
    Tasks are created with a task title, description, due date, current date
    and the status of each task is incomplete.

    Returns:
        due_date(date.time.date): The due date that the user enters.
    """
    # Initialize an empty list to store the current task titles.
    current_titles_list = []

    # Request user to enter a username, until they enter an existing user.
    while True:
        assigned_to = input(
            "Please enter the username of the person whom the task is"
            " assigned to: \n"
        ).strip().lower()

        # Check if the username is in the user_data dictionary
        if assigned_to.lower() not in user_data:
            print("The user does not exist. Enter a registered username.")
            continue
        break       # Exit if the username is valid.

    try:
        # Open the 'tasks.txt' file in read mode.
        with open("tasks.txt", "r", encoding='utf-8') as file:

            # Loop through each line of the 'tasks.txt' file
            # and get the title of each task.
            for line in file:
                elements = line.strip().split(", ")
                current_titles = elements[1].lower()

                # Save each task title to the 'current_titles' list.
                current_titles_list.append(current_titles)

    except FileNotFoundError:
        print("The tasks.txt file was not found.")

    # Request the user to enter a title for the task.
    while True:
        task_title = input("Please enter the title of the task: \n").strip()

        # Restart the loop if the title already exists.
        if task_title.lower() in current_titles_list:
            print("This title already exists. Please enter a new title")
            continue

        # Restart the loop if the title is blank.
        if not task_title:
            print("This field cannot be blank.")
            continue

        # Restart the loop if the title only consists of number.
        if task_title.isnumeric():
            print("This field cannot only consist of numbers")
            continue
        break

    # Request user to enter the task description.
    while True:
        task_description = input(
            "Please enter the description of the task: \n"
        ).strip()

        # Restart the loop if the description is blank.
        if not task_description:
            print("This field cannot be blank")
            continue

        # Restart the loop if the task description only consists of number.
        if task_description.isnumeric():
            print("This field cannot only consist of numbers")
            continue
        break

    # Request the user to input the due date.
    while True:
        due_date = input(
            "Please enter the due date in the format"
            " DD Mon YYYY (eg. 07 Mar 2001): \n"
        ).strip()

        try:
            # Change the input string into a date object
            due_date = datetime.strptime(due_date, "%d %b %Y").date()
            break       # Exit if the change is successful.

        # If the format is not correct, restart the loop
        except ValueError:
            print("Invalid date format. Please use DD Mon YYYY"
                  " (e.g., 07 Mar 2001).")

    # Get current date
    current_date = date.today()

    # Format the current date to a string format
    date_today = current_date.strftime("%d %b %Y")

    # Initialize task completion status to no.
    complete_task = "no"

    try:
        # Open 'tasks.txt' and append the new task to the file
        with open("tasks.txt", "a", encoding='utf-8') as file:
            file.write(
                "\n" + assigned_to + "," + " " +
                task_title + "," + " " +
                task_description + "," + " " +
                date_today + "," + " " +
                due_date.strftime("%d %b %Y") + "," + " " +
                complete_task
            )
        print("The task was successfully added to the tasks.txt file.")
    except FileNotFoundError:
        print("The tasks.txt file was not found.")

    return due_date


def view_all():
    """
    Reads all information in 'tasks.txt' and displays each task in detail.

    """
    try:
        # Open the 'tasks.txt' file in read mode.
        with open('tasks.txt', 'r', encoding='utf-8') as file:

            # Iterate through each line in the file and split into elements.
            for line in file:
                elements = line.strip().split(", ")

                # Check that each line has 6 elements.
                if len(elements) == 6:

                    # Print seperation line.
                    print("-" * 150)

                    # Print each element for each line.
                    print(f"{'Task:' :<20} {elements[1] :<10}")
                    print(f"{'Assigned to:':<20} {elements[0] :<10}")
                    print(f"{'Date Assigned:' :<20} {elements[3] :<10}")
                    print(f"{'Due Date:' :<20} {elements[4] :<10}")
                    print(f"{'Task Complete:' :<20} {elements[5] :<10}")
                    print(f"{'Task Description:' :<20} {elements[2] :<10}")
                    print("-" * 150)

    except FileNotFoundError:
        print("The tasks.txt file was not found.")


def view_mine(username):
    """
    Allows the user to view and edit all tasks assigned to them.

    The user is able to mark their tasks as complete.
    If the task is incomplete the user is able to edit the assignee
    and the due date.

    Parameters:
        username (str): The user that is logged in.
    """
    # Create a flag to check if the task was found.
    tasks_found = False

    # Variable to store and display the task count.
    task_number = 0

    # List that stores the actual index of each line in the file.
    actual_task_number = []

    try:

        # Open the 'tasks.txt' file in read mode.
        with open('tasks.txt', 'r', encoding='utf-8') as file:
            tasks = file.readlines()

            # Iterate through the tasks in each line and check if its
            # assigned to the logged-in user.
            for index, line in enumerate(tasks):
                elements = line.strip().split(", ")

                if username == elements[0]:
                    tasks_found = True

                    # Print the details of each task
                    print("-" * 150)
                    print(f"{'Task Number:' :<20} {task_number}")
                    print(f"{'Task:' :<20} {elements[1] :<10}")
                    print(f"{'Assigned to:':<20} {elements[0] :<10}")
                    print(f"{'Date Assigned:' :<20} {elements[3] :<10}")
                    print(f"{'Due Date:' :<20} {elements[4] :<10}")
                    print(f"{'Task Complete:' :<20} {elements[5] :<10}")
                    print(f"{'Task Description:' :<20} {elements[2] :<10}")
                    print("-" * 150)

                    # Save the index of the task in the file
                    actual_task_number.append(index)
                    # Increase the task count by 1 for the count shown to user.
                    task_number += 1

            # Print message if no tasks were found for user.
            if tasks_found is False:
                print("There are no tasks for this user")
                return

    # Print error message if the file was not found.
    except FileNotFoundError:
        print("The tasks.txt file was not found.")

    # Recursive function to get valid task selection
    def get_valid_task_selection():
        try:

            # Request user to enter the number of the task they want to select.
            task_selection = int(input(
                "Please enter the number of the task you want to select or "
                "enter -1 to return to the main menu: \n"
            ).strip())

            # Base case - returns to main menu
            if task_selection == -1:
                return -1

            # Check if the input is greater than 0 but less than the actual
            # number of tasks.
            if 0 <= task_selection < len(actual_task_number):
                return task_selection
            else:
                print("Invalid task number. Please try again.")
                return get_valid_task_selection()

        except ValueError:
            print("Invalid input. Please enter a valid task number.")
            return get_valid_task_selection()

    # Get the user's task selection.
    task_selection = get_valid_task_selection()
    if task_selection == -1:
        return

    # Get the index of the task selected by the user.
    file_index = actual_task_number[task_selection]
    elements = tasks[file_index].strip().split(", ")

    # Check if the user wants to mark the task as complete or edit the task.
    complete_or_edit = input(
        "Would you like to mark this task as complete or edit the task) (C/E)"
    ).strip().lower()

    # Check if the task is completed.
    # No changes can be made to completed tasks.
    if elements[5] == "yes":
        print("No changes can be made as the task is complete")
        return

    # Change task status to complete.
    if complete_or_edit == "c":
        elements[5] = "yes"

        # Update and replace the original task in the list.
        tasks[file_index] = ", ".join(elements) + "\n"
        print("This task is now complete")

    # If the user chooses to edit, request them to input a new name
    # and or new due date.
    elif complete_or_edit == "e":
        new_assignee = input(
            "Please enter the name of the new assignee or leave blank to keep "
            "the same: \n"
        ).strip()
        new_due_date = input(
            "Please enter the new due date (leave blank to keep the same): \n"
        ).strip()

        # Update the "assigned_to" position with the new_assignee.
        if new_assignee:
            elements[0] = new_assignee

        # Update the "due_date" position with the new due date.
        if new_due_date:
            elements[4] = new_due_date

        # Update and replace the original task in the list.
        tasks[file_index] = ", ".join(elements) + "\n"
        print("The task was successfully edited")

    else:
        print(
            "Invalid option. Please enter 'c' to complete the task or "
            "'e' to edit the task."
        )

    # Write the updated task to the task.txt file
    with open('tasks.txt', 'w', encoding='utf-8') as file:
        file.writelines(tasks)


def view_completed():
    """
    This function displays all completed tasks.
    """
    try:
        # Open the 'tasks.txt' file in read mode.
        with open('tasks.txt', 'r', encoding='utf-8') as file:

            # Create a flag to track completed tasks.
            complete_tasks = False

            # Loop through each line in the file and split into elements.
            for line in file:
                elements = line.strip().split(", ")

                # Check if the task has 6 elements and is completed.
                if len(elements) == 6 and elements[5].lower() == "yes":

                    # Change flag to True when completed tasks are found.
                    complete_tasks = True

                    # Print each task
                    print("-" * 150)
                    print(f"{'Task:' :<20} {elements[1] :<10}")
                    print(f"{'Assigned to:':<20} {elements[0] :<10}")
                    print(f"{'Date Assigned:' :<20} {elements[3] :<10}")
                    print(f"{'Due Date:' :<20} {elements[4] :<10}")
                    print(f"{'Task Complete:' :<20} {elements[5] :<10}")
                    print(f"{'Task Description:' :<20} {elements[2] :<10}")
                    print("-" * 150)

            # Print response to no tasks being found.
            if complete_tasks is False:
                print("There are no complete tasks")

    # Print error if file does not exist.
    except FileNotFoundError:
        print("No removed_tasks.txt found.")


def delete_task():
    """
    This function will allow the user to delete a task from the tasks.txt file.
    The user will be prompted to enter the task title they wish to delete.
    If the task is found, it will be removed from the file.
    """
    # Create a list to store the index of each task.
    task_pos = []

    try:
        # Open file in read mode.
        with open('tasks.txt', 'r', encoding='utf-8') as file:
            tasks_list = file.readlines()

        # Check if the tasks file is empty and print message.
        if not tasks_list:
            print("There are no current task for deletion")
            return

        # Iterate through each line in the list with its index,
        # using enumerate.
        for index, line in enumerate(tasks_list):
            elements = line.strip().split(", ")

            # Check that each line has 6 elements.
            if len(elements) == 6:

                # Print all current tasks.
                print("Current Tasks")
                print("-" * 150)
                print(f"{'Task Number:' :<20} {len(task_pos)}")
                print(f"{'Task:' :<20} {elements[1] :<10}")
                print(f"{'Assigned to:':<20} {elements[0] :<10}")
                print(f"{'Date Assigned:' :<20} {elements[3] :<10}")
                print(f"{'Due Date:' :<20} {elements[4] :<10}")
                print(f"{'Task Complete:' :<20} {elements[5] :<10}")
                print(f"{'Task Description:' :<20} {elements[2] :<10}")
                print("-" * 150)

                # Track the index of each task and append to the task_pos list.
                task_pos.append(index)

        # Print message and exit if there are no tasks found.
        if not task_pos:
            print("There are no tasks found")
            return

        # Continue to the request the user to enter a valid input.
        while True:
            try:
                task_to_remove = int(input(
                    "Please enter the number of the task you want to delete "
                    "or -1 to cancel: \n"
                ).strip())

                # Exit if the user chooses to cancel.
                if task_to_remove == -1:
                    print("Operation cancelled. No tasks deleted")
                    return

                # Check if the number selected is greater than or equal to 0
                # and less than the actual number of tasks.
                if 0 <= task_to_remove < len(task_pos):
                    break

                else:
                    print("Invalid task number. Please try again.")

            except ValueError:
                print("Invalid input. Please enter a valid task number.")

    except FileNotFoundError:
        print("The tasks.txt file was not found")

    # Get the index of the line that the user selected.
    task_to_delete = task_pos[task_to_remove]

    # Delete the selected task from the list.
    removed = tasks_list.pop(task_to_delete)

    try:
        # Update the "tasks.txt" file with the the updated list.
        with open("tasks.txt", "w", encoding='utf-8') as file:
            file.writelines(tasks_list)

        # Print success message.
        print("The task below was successfully deleted")
        print(removed)
    except FileNotFoundError:
        print("The tasks.txt file could not be found")


def get_task_stats():
    """
    Reads the 'tasks.txt' and calculates the task statistics.

    A dictionary is returned with the following:
        total_tasks: The total number of tasks
        total_complete: The total of tasks that is marked as complete.
        total_incomplete: The total of tasks that is incomplete.
        total_incomplete_overdue: Tasks that are both overdue and incomplete.
        percentage_incomplete: Percentage of tasks that are incomplete.
        percentage_overdue: Percentage of tasks that are overdue.
        tasks_list: List all the tasks from the file
    """
    try:
        # Open file in read mode.
        with open('tasks.txt', 'r', encoding='utf-8') as file:
            tasks = file.readlines()

    except FileNotFoundError:
        print("The tasks.txt file was not found.")
        return

    # Get the total number of tasks.
    total_tasks = len(tasks)

    # Initialize the task counters to 0.
    total_complete = 0
    total_incomplete = 0
    total_overdue = 0
    total_incomplete_overdue = 0

    # Loop through each task and split into elements.
    for task in tasks:
        elements = task.strip().split(", ")

        # If there are 6 elements and that the task is complete
        # increase the total_complete counter by 1.
        if len(elements) == 6 and elements[5].lower() == "yes":
            total_complete += 1

        # If there are 6 elements and that the task is incomplete
        # increase the total_incomplete counter by 1.
        elif len(elements) == 6 and elements[5].lower() == "no":
            total_incomplete += 1

        try:
            # Change the due_date string into a date object.
            due_date = datetime.strptime(elements[4], "%d %b %Y").date()

            # If the due date is passed and the task is incomplete
            # increase the total_incomplete_overdue counter by 1.
            if (
                due_date < datetime.today().date() and
                elements[5].lower() == "no"
            ):
                total_incomplete_overdue += 1

            # If the due date is passed, increase the total_overdue
            # counter by 1.
            if due_date < datetime.today().date():
                total_overdue += 1

        except ValueError:
            print(f"Invalid date format in task: {elements[4]}")
            continue

    # If the total tasks are greater than zero, calculate the percentages
    # of incomplete tasks and overdue tasks.
    if total_tasks > 0:
        percentage_incomplete = (total_incomplete / total_tasks) * 100
        percentage_overdue = (total_overdue / total_tasks) * 100

    else:
        percentage_incomplete = 0
        percentage_overdue = 0

    # Return a statistical values as a dictionary.
    return {
        "total_tasks": total_tasks,
        "total_complete": total_complete,
        "total_incomplete": total_incomplete,
        "total_incomplete_overdue": total_incomplete_overdue,
        "percentage_incomplete": percentage_incomplete,
        "percentage_overdue": percentage_overdue,
        "tasks_list": tasks
    }


def get_user_stats(tasks_list):
    """
    Calculates the statistics for each user based on the task list.

    The function finds the following statistics for each user:
    - The total number of tasks assigned.
    - Percentage of total tasks assigned.
    - Percentage of tasks complete.
    - Percentage of tasks incomplete.
    - Percentage of tasks incomplete and overdue

    Parameters:
    tasks_list (list): Each line in the 'tasks.txt file is saved in the list.


    Returns:
        dict:
            -'total_users': The total number of registered users.
            - 'user_stats': Nested dictionary with the stats for each user.
    """
    # Create  an empty list to store usernames.
    users = []

    try:
        # Open the 'user.txt. file in read mode.
        with open('user.txt', 'r', encoding='utf-8') as file:

            # Iterate through each line and split the line into elements.
            for line in file:
                elements = line.strip().split(", ")

                # Store each username in the users list.
                users.append(elements[0].lower())

    except FileNotFoundError:
        print("The user.txt file was not found.")
        return

    # Calculate the total number of users and tasks.
    total_users = len(users)
    total_tasks = len(tasks_list)

    # Create a dictionary to store the statistics for each user.
    user_stats = {}

    for name_of_user in users:
        # Create counters for each user and initialize to 0.
        users_total_tasks = 0
        users_completed_tasks = 0
        users_incomplete_tasks = 0
        user_overdue_incomplete = 0

        # Iterate through each task in the task list.
        for task in tasks_list:
            elements = task.strip().split(", ")

            # If lines do not have 6 elements, skip the line.
            if len(elements) != 6:
                continue

            # Save who the task is assigned to in a variable.
            task_assignee = elements[0].strip().lower()

            # Save the status of the task in a variable.
            task_status = elements[5].strip().lower()

            # Check if the task is assigned to the current user.
            if task_assignee == name_of_user:

                # Increase the total task counter by 1.
                users_total_tasks += 1

                # If the task is complete, increase the respective
                # counter by 1.
                if task_status == "yes":
                    users_completed_tasks += 1

                # If the task is incomplete, increase the respective
                # counter by 1.
                elif task_status == "no":
                    users_incomplete_tasks += 1

                    try:
                        # Change the due date string to a date object.
                        user_due_date = datetime.strptime(
                            elements[4], "%d %b %Y"
                        ).date()

                        # Check if the task is overdue (if the due date is
                        # less than the current date).
                        if (
                            user_due_date < datetime.today().date() and
                            elements[5].lower() == "no"
                        ):
                            user_overdue_incomplete += 1

                    except ValueError:
                        print(f"Invalid date format in task: {elements[4]}")
                        continue

        # Calculate percentage of tasks assigned to each user.
        if total_tasks > 0:
            user_percentage_assigned = (users_total_tasks / total_tasks) * 100
        else:
            user_percentage_assigned = 0

        # If the total tasks is greater than 0,
        # calculate the following percentages.
        if users_total_tasks > 0:

            # Percentage of completed tasks.
            user_percentage_completed = (
                users_completed_tasks / users_total_tasks
            ) * 100

            # Percentage of incomplete tasks.
            user_percentage_incomplete = (
                users_incomplete_tasks / users_total_tasks
            ) * 100

            # Percentage of incomplete and overdue tasks.
            user_percentage_overdue_incomplete = (
                user_overdue_incomplete / users_total_tasks
            ) * 100
        else:

            # If there are no tasks, all percentages equal to 0.
            user_percentage_completed = 0
            user_percentage_incomplete = 0
            user_percentage_overdue_incomplete = 0

        # Save the user's stats.
        user_stats[name_of_user] = {
            "total_tasks": users_total_tasks,
            "percentage_assigned": user_percentage_assigned,
            "percentage_completed": user_percentage_completed,
            "percentage_incomplete": user_percentage_incomplete,
            "percentage_overdue_incomplete": user_percentage_overdue_incomplete
        }

    # Return all the stats in a dictionary.
    return {
        "total_users": total_users,
        "user_stats": user_stats
    }


def generate_report():
    """
    This function generates the task_overview.txt file and the
    user_overview.txt file.

    The function calls get_task_stats() and  get_user_stats()
    to get the task and user statstics. The information is then written into
    the respective files.

    task_overview.txt - consists of stats for all the tasks.
    user_overview.txt - consists of stats for each specific user.

    Error messages are printed if the retrieval or writing to the text file
    fails.
    """

    # Call get_task_stats() to retrieve the tasks statistics.
    tasks_stats = get_task_stats()
    if not tasks_stats:
        return      # Exit if there are no statistics.

    # Call get_user_stats() to retrieve the statistics for each user.
    user_stats = get_user_stats(tasks_stats["tasks_list"])
    if not user_stats:
        return      # Exit if there are no statistics.

    # ========== Task Overview Report ==========
    try:
        # Open the 'task_overview.txt. file in write mode.
        with open('task_overview.txt', 'w', encoding='utf-8') as file:

            # Write the totals and percentages of all the tasks, to the file.
            file.write("Task Overview Report\n")

            file.write(f"{'-'* 20}\n")

            file.write(
                f"Total number of tasks: {tasks_stats['total_tasks']}\n"
            )

            file.write(
                f"Total number of completed tasks: "
                f"{tasks_stats['total_complete']}\n"
            )

            file.write(
                f"Total number of incompleted tasks: "
                f"{tasks_stats['total_incomplete']}\n"
            )

            file.write(
                f"Total number of tasks that are incomplete and overdue: "
                f"{tasks_stats['total_incomplete_overdue']}\n"
            )

            file.write(
                f"Percentage of incomplete tasks: "
                f"{tasks_stats['percentage_incomplete']:.2f}%\n"
            )

            file.write(
                f"Percentage of overdue tasks: "
                f"{tasks_stats['percentage_overdue']:.2f}%\n"
            )

            file.write(f"{'-'* 20}")

    # Print an error message for file related errors.
    except OSError as error:
        print(f"Could not write to task_over.txt: {error}")
        return

    # Print success message.
    print("The task overview report has been created.")

    # ========== User Overview Report ==========
    try:
        # Open 'user_overview.txt' in write mode.
        with open('user_overview.txt', 'w', encoding='utf-8') as file:

            file.write("User Overview Report\n")
            file.write(f"{'-'* 20}\n")

            # Write the total number of registered users and total number of
            # tasks to the file.
            file.write(
                f"Total users registered on Task Manager: "
                f"{user_stats['total_users']}\n"
            )

            file.write(
                f"Total number of tasks generated on Task Manager: "
                f"{tasks_stats['total_tasks']}\n"
            )

            # Iterate through each user and write their specific statistics to
            # the file.
            for user, stats in user_stats["user_stats"].items():
                file.write(f"\nUser: {user}\n")

                file.write(f"Total tasks assigned: {stats['total_tasks']}\n")

                file.write(
                    f"Percentage of tasks assigned: "
                    f"{stats['percentage_assigned']:.2f}%\n"
                )

                file.write(
                    f"Percentage of tasks completed: "
                    f"{stats['percentage_completed']:.2f}%\n"
                )

                file.write(
                    f"Percentage of tasks incomplete: "
                    f"{stats['percentage_incomplete']:.2f}%\n"
                )

                file.write(
                    f"Percentage of overdue and incomplete tasks: "
                    f"{stats['percentage_overdue_incomplete']:.2f}%\n"
                )

                file.write(f"{'-'* 20}\n")

    # Print an error message for file related errors.
    except OSError as error:
        print(f"Could not write to user_overview.txt: {error}")
        return

    # Print success message.
    print("The user overview report has been created.")


def display_statistics():
    """
    Print the tasks statistics and user statistic reports on the console.

    Call get_task_stats() and get_user_stats() to retrieve the respective
    statistics and print to the console.

    If the retrieval fails, print an error message and exit.
    """

    # Call get_task_stats() to retrieve the task statistics.
    tasks_stats = get_task_stats()

    # If task statistics could not be retrieved, exit.
    if not tasks_stats:
        print("Could not fetch task stats")
        return

    # Call get_user_stats() to retrieve statistics for each user.
    user_stats = get_user_stats(tasks_stats["tasks_list"])

    # If user statistics could not be retrieved, exit.
    if not user_stats:
        return

    # ========== Task Overview ==========
    print("Task Overview Report\n")
    print(f"{'-'* 20}\n")

    # Print the totals and percentages of all the tasks, on the console.
    print(
        f"Total number of tasks: {tasks_stats['total_tasks']}\n"
    )

    print(
        f"Total number of completed tasks: {tasks_stats['total_complete']}\n"
    )

    print(
        f"Total number of incompleted tasks: "
        f"{tasks_stats['total_incomplete']}\n"
    )

    print(
        f"Total number of tasks that are incomplete and overdue: "
        f"{tasks_stats['total_incomplete_overdue']}\n"
    )

    print(
        f"Percentage of incomplete tasks: "
        f"{tasks_stats['percentage_incomplete']:.2f}%\n"
    )

    print(
        f"Percentage of overdue tasks: "
        f"{tasks_stats['percentage_overdue']:.2f}%\n"
    )

    print(f"{'-'* 20}")

    # ========== User Overview ==========
    print("User Overview Report\n")
    print(f"{'-'* 20}\n")

    # Print the total number of registered users and total number of
    # tasks, on the console.
    print(
        f"Total users registered on Task Manager: "
        f"{user_stats['total_users']}\n"
    )

    print(
        f"Total number of tasks generated on Task Manager: "
        f"{tasks_stats['total_tasks']}\n")

    print(f"{'-'* 20}\n")

    # Iterate through each user and print their specific statistics,
    # on the console.
    for user, stats in user_stats["user_stats"].items():
        print(f"\nUser: {user}\n")
        print(f"Total tasks assigned: {stats['total_tasks']}\n")

        print(
            f"Percentage of tasks assigned: "
            f"{stats['percentage_assigned']:.2f}%\n"
        )

        print(
            f"Percentage of tasks completed: "
            f"{stats['percentage_completed']:.2f}%\n"
        )

        print(
            f"Percentage of tasks incomplete: "
            f"{stats['percentage_incomplete']:.2f}%\n"
        )

        print(
            f"Percentage of overdue and incomplete tasks: "
            f"{stats['percentage_overdue_incomplete']:.2f}%\n"
        )

        print(f"{'-'* 20}\n")

# ========== Function Calls ==========


# Call read_user_data() to read the user data.
read_user_data()

# Call login() and save the username that logged in.
user_logged_in = login()

# If the user that logged in is the admin user load the admin menu.
if user_logged_in == "admin":
    admin_menu(user_logged_in)

# Else show the user menu.
else:
    user_menu(user_logged_in)

# References:
# 1. https://stackoverflow.com/q/46710542
# 2. https://docs.python.org/3/tutorial/errors.html
# 3. https://www.programiz.com/python-programming/datetime/current-datetime
