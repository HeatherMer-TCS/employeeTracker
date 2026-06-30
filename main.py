import sqlite3
from pathlib import Path
from datetime import datetime
from flask import Flask, jsonify, abort, request, redirect, url_for, render_template

DB_PATH = Path(__file__).with_name("employee_tracker.db")

app = Flask(__name__)

# Connect to the SQLite database and return a connection object
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Validate that the form date is in the correct format
def validate_iso_date(value):
    if value is None or value == "":
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
    except ValueError:
        raise ValueError("hire_date must be YYYY-MM-DD")

# Ensure all falsey form values are converted to None
def normalize_value(value):
    if value in (None, "", "None"):
        return None
    return value

# Flask route to display the home page
@app.route("/")
def index():
    message = request.args.get("message")
    message_type = request.args.get("message_type")

    update_employee = {
        "employee_id": request.args.get("update_employee_id", ""),
        "first_name": request.args.get("first_name", ""),
        "last_name": request.args.get("last_name", ""),
        "email": request.args.get("email", ""),
        "phone_number": request.args.get("phone_number", ""),
        "hire_date": request.args.get("hire_date", ""),
        "job_id": request.args.get("job_id", ""),
        "salary": request.args.get("salary", ""),
        "commission_pct": request.args.get("commission_pct", ""),
        "manager_id": request.args.get("manager_id", ""),
        "department_id": request.args.get("department_id", ""),
    }
    delete_employee_id = request.args.get("delete_employee_id", "")

    return render_template(
        "index.html",
        message=message,
        message_type=message_type,
        update_employee=update_employee,
        delete_employee_id=delete_employee_id,
    )

# Flask route to display employees
@app.route("/employees", methods=["GET"])
def employees():
    # GET table of employees from database
    with get_db_connection() as conn:
        rows = conn.execute("SELECT * FROM employees").fetchall()
    data = [
        {key: normalize_value(value) for key, value in dict(row).items()}
        for row in rows
    ]
    if request.args.get("format") == "json":
        return jsonify(data)
    return render_template("employees.html", employees=data, count=len(data))


@app.route("/employees/new", methods=["POST"])
def add_employee():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    phone_number = request.form.get("phone_number")
    hire_date = request.form.get("hire_date")
    job_id = request.form.get("job_id")
    salary = request.form.get("salary")
    commission_pct = request.form.get("commission_pct")
    manager_id = request.form.get("manager_id")
    department_id = request.form.get("department_id")

    try:
        hire_date = validate_iso_date(hire_date)
    except ValueError:
        return "Invalid hire_date, must be YYYY-MM-DD", 400

    try:
        salary = float(salary) if salary else None
    except (TypeError, ValueError):
        return "Invalid salary", 400

    try:
        commission_pct = float(commission_pct) if commission_pct else None
    except (TypeError, ValueError):
        return "Invalid commission_pct", 400

    try:
        manager_id = int(manager_id) if manager_id else None
    except (TypeError, ValueError):
        return "Invalid manager_id", 400

    try:
        department_id = int(department_id) if department_id else None
    except (TypeError, ValueError):
        return "Invalid department_id", 400

    with get_db_connection() as conn:
        conn.execute(
            "INSERT INTO employees (first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                first_name,
                last_name,
                email,
                phone_number,
                hire_date,
                job_id,
                salary,
                commission_pct,
                manager_id,
                department_id,
            ),
        )

    return redirect(url_for("index", message="Employee added successfully", message_type="success"))


@app.route("/employees/update", methods=["POST"])
def update_employee():
    employee_id = request.form.get("employee_id")
    if not employee_id:
        return redirect(url_for("index", message="Employee ID is required", message_type="error"))

    try:
        employee_id = int(employee_id)
    except ValueError:
        return redirect(url_for("index", message="Invalid employee ID", message_type="error"))

    with get_db_connection() as conn:
        row = conn.execute(
            "SELECT * FROM employees WHERE employee_id = ?",
            (employee_id,),
        ).fetchone()
        if row is None:
            return redirect(url_for("index", message="Employee not found", message_type="error"))

        first_name = request.form.get("first_name") or row["first_name"]
        last_name = request.form.get("last_name") or row["last_name"]
        email = request.form.get("email") or row["email"]
        phone_number = request.form.get("phone_number") or row["phone_number"]
        hire_date = request.form.get("hire_date") or row["hire_date"]
        job_id = request.form.get("job_id") or row["job_id"]
        salary = request.form.get("salary") or row["salary"]
        commission_pct = request.form.get("commission_pct") or row["commission_pct"]
        manager_id = request.form.get("manager_id") or row["manager_id"]
        department_id = request.form.get("department_id") or row["department_id"]

    try:
        hire_date = validate_iso_date(hire_date)
    except ValueError:
        return "Invalid hire_date, must be YYYY-MM-DD", 400

    try:
        salary = float(salary) if salary is not None and salary != "" else None
    except (TypeError, ValueError):
        return "Invalid salary", 400

    try:
        commission_pct = float(commission_pct) if commission_pct is not None and commission_pct != "" else None
    except (TypeError, ValueError):
        return "Invalid commission_pct", 400

    try:
        manager_id = int(manager_id) if manager_id is not None and manager_id != "" else None
    except (TypeError, ValueError):
        return "Invalid manager_id", 400

    try:
        department_id = int(department_id) if department_id is not None and department_id != "" else None
    except (TypeError, ValueError):
        return "Invalid department_id", 400

    with get_db_connection() as conn:
        cursor = conn.execute(
            "UPDATE employees SET first_name = ?, last_name = ?, email = ?, phone_number = ?, hire_date = ?, job_id = ?, salary = ?, commission_pct = ?, manager_id = ?, department_id = ? WHERE employee_id = ?",
            (
                first_name,
                last_name,
                email,
                phone_number,
                hire_date,
                job_id,
                salary,
                commission_pct,
                manager_id,
                department_id,
                employee_id,
            ),
        )
        updated_rows = cursor.rowcount

    if updated_rows == 0:
        return redirect(url_for("index", message="Employee not found", message_type="error"))

    return redirect(url_for("index", message="Employee updated successfully", message_type="success"))


@app.route("/employees/delete", methods=["POST"])
def delete_employee():
    employee_id = request.form.get("employee_id")
    confirmation = request.form.get("confirm")
    if not employee_id:
        return redirect(url_for("index", message="Employee ID is required", message_type="error"))
    
    # Check if the confirmation text is correct
    if confirmation != "DELETE":
        return redirect(url_for("index", message="Confirmation text is incorrect. Type 'DELETE' to confirm.", message_type="error"))

    # Validate that the employee_id is an integer
    try:
        employee_id = int(employee_id)
    except ValueError:
        return redirect(url_for("index", message="Invalid employee ID", message_type="error"))

    # Delete the employee from the database
    with get_db_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM employees WHERE employee_id = ?",
            (employee_id,),
        )
        deleted_rows = cursor.rowcount

    if deleted_rows == 0:
        return redirect(url_for("index", message="Employee not found", message_type="error"))

    return redirect(url_for("index", message="Employee removed successfully", message_type="success"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)