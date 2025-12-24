# Student Management System (CRUD)

A simple yet feature-rich Student Management System built with Python, Flask, and SQLite. This application allows you to perform CRUD (Create, Read, Update, Delete) operations on student records with a modern user interface powered by Bootstrap 5.

## Features

- **CRUD Operations**: Add, view, update, and delete student records.
- **Search**: Filter students by name.
- **Sorting**: Sort the student list by Name or Branch (Ascending/Descending).
- **Pagination**: Efficiently browse through large lists of students.
- **Export to CSV**: Download the student list (filtered or full) as a CSV file.
- **Responsive Design**: Clean and mobile-friendly UI using Bootstrap 5.
- **Flash Messages**: Instant feedback for user actions (e.g., "Student Added Successfully").

## Prerequisites

- Python 3.x installed on your system.

## Installation

1.  **Navigate to the project directory**:

    ```bash
    cd student_crud
    ```

2.  **Create a virtual environment** (recommended):

    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1.  **Start the Flask server**:

    ```bash
    python app.py
    ```

2.  **Access the application**:
    Open your web browser and go to `http://127.0.0.1:5000/`.

## Project Structure

- `app.py`: The main Flask application file containing routes and database logic.
- `database.db`: SQLite database file (created automatically on first run).
- `requirements.txt`: List of Python dependencies.
- `templates/`: HTML templates for the application.
