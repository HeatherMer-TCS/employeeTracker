# Employee Database Management System

A simple Flask application for tracking employees in a local SQLite database.

Features:
- View all employees
- Add a new employee
- Update employee details
- Delete an employee with confirmation
- Live filtering across all employee fields
- Optional JSON API for employee data

## Requirements

- Python 3.9 or newer
- `flask` package
- `requests` package (declared dependency in `pyproject.toml`)
- Optional: `uv` for running scripts with `uv run`

## Setup

**Using pip:**

1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
python -m pip install flask
```

**Using uv:**

Create a virtual environment and install dependecies with 

```powershell
uv sync
```

## Database Setup

The app uses the local SQLite database file `employee_tracker.db`. This file may have been modified.

To start fresh, recreate and repopluate the employees from the provided `employees.csv` file using `setupDatabase.py`. Run:

**Using python:**

```powershell
python setupDatabase.py
```

**Using `uv`:**

```powershell
uv run setupDatabase.py
```

This script drops and recreates the `employees` table, then loads data from `employees.csv`.

## Run Application

**Using python**

```powershell
python main.py
```

**Using `uv`:**

```powershell
uv run main.py
```

Then open `http://127.0.0.1:5000` in your browser.

## API Endpoint

The app serves the employee list at:

- `GET /employees` — renders the employee table in HTML
- `GET /employees?format=json` — returns employee data as JSON

## Notes

- The delete form requires typing `DELETE` in the confirmation field before an employee can be removed.
- If `uv` is not installed, use `python ...` commands instead.

## Files

- `main.py` — Flask app and routes
- `setupDatabase.py` — creates `employee_tracker.db` from `employees.csv`
- `employees.csv` — source data for the database
- `templates/` — HTML templates for the UI
- `static/styles.css` — application stylesheet