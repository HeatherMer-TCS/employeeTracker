import csv
import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).with_name("employee_tracker.db")
CSV_PATH = Path(__file__).with_name("employees.csv")

# SQL command to create the employees table
CREATE_SQL = """
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone_number TEXT,
    hire_date TEXT,
    job_id TEXT,
    salary REAL,
    commission_pct REAL,
    manager_id INTEGER,
    department_id INTEGER
)
"""

# Function to parse values from CSV and convert them to the appropriate type
def parse_value(value, value_type):
    if value is None:
        return None
    text = value.strip()
    if text == "" or text == "-":
        return None
    if value_type is int:
        return int(text)
    if value_type is float:
        return float(text)
    return text

# Function to load CSV data into SQLite database
def load_csv_to_sqlite(csv_path=CSV_PATH, db_path=DB_PATH):
    with sqlite3.connect(db_path) as conn:
        conn.execute("DROP TABLE IF EXISTS employees")
        conn.execute(CREATE_SQL)

        with csv_path.open(newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            rows = []
            for row in reader:
                rows.append(
                    (
                        parse_value(row["EMPLOYEE_ID"], int),
                        parse_value(row["FIRST_NAME"], str),
                        parse_value(row["LAST_NAME"], str),
                        parse_value(row["EMAIL"], str),
                        parse_value(row["PHONE_NUMBER"], str),
                        parse_value(row["HIRE_DATE"], str),
                        parse_value(row["JOB_ID"], str),
                        parse_value(row["SALARY"], float),
                        parse_value(row["COMMISSION_PCT"], float),
                        parse_value(row["MANAGER_ID"], int),
                        parse_value(row["DEPARTMENT_ID"], int),
                    )
                )

        conn.executemany(
            """
            INSERT INTO employees (
                employee_id,
                first_name,
                last_name,
                email,
                phone_number,
                hire_date,
                job_id,
                salary,
                commission_pct,
                manager_id,
                department_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
    print(f"Created database {db_path} and loaded {len(rows)} rows from {csv_path}.")


def main():
    load_csv_to_sqlite()


if __name__ == "__main__":
    main()
