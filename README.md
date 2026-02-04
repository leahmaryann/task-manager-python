# Task Manager Application

## Overview
This project is a command-line Task Manager application built in Python. It allows users to log in, view assigned tasks, and manage task completion or edits based on their role. The system uses file-based storage to persist user and task data.

## Features
- User authentication
- Role-based access (admin vs standard user)
- View tasks assigned to the logged-in user
- Mark tasks as complete
- Edit task descriptions
- File-based data persistence using text files
- Input validation and error handling

## How the Application Works
- User and task information is stored in text files (`users.txt`, `tasks.txt`)
- Each task contains:
  - Assigned user
  - Task title
  - Task description
  - Date assigned
  - Due date
  - Completion status
- Users can only view and modify tasks assigned to them
- Admin users have access to additional management options

## Example Functionality
The `view_mine()` function:
- Reads task data from a file
- Displays tasks assigned to the logged-in user in a formatted layout
- Allows users to select a task
- Enables marking a task as complete or editing the task description
- Updates the task file accordingly

## Technologies Used
- Python
- File I/O
- Control flow and loops
- Functions and modular logic
- Error handling (try/except)

## How to Run
1. Ensure Python 3 is installed
2. Clone this repository
3. Run the main Python file

## Future Improvements
- Refactor file storage to a database
- Improve menu navigation and UX
- Add task deletion and due date validation

