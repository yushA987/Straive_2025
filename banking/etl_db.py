import pandas as pd
import sqlite3
import os

CSV_FILE = "data.csv"
DB_FILE = "employees.db"
TABLE_NAME = "employees"

# STEP 1: Load CSV
try:
    df = pd.read_csv(CSV_FILE)
    print("Initial Data:")
    print(df.head())
except FileNotFoundError:
    print(f"{CSV_FILE} not found")
    exit()
except pd.errors.EmptyDataError:
    print(f"{CSV_FILE} is empty")
    exit()
except Exception as e:
    print(f"Unknown error during CSV load: {e}")
    exit()

# STEP 2: Transform Data
try:
    curr_year = 2025
    print("Before Transformation Types:\n", df.dtypes)

    df["DOB"] = pd.to_datetime(df["DOB"])
    df["JoinDate"] = pd.to_datetime(df["JoinDate"])

    df["Age"] = curr_year - df["DOB"].dt.year
    df["YearOfService"] = curr_year - df["JoinDate"].dt.year

    df["Salary"] = df["Salary"].astype(float)

    print("After Transformation:\n", df.head())

except KeyError as e:
    print(f"Missing column: {e}")
    exit()
except ValueError as e:
    print(f"Value conversion failed: {e}")
    exit()
except Exception as e:
    print(f"Unknown transformation error: {e}")
    exit()

# STEP 3: Load to SQLite DB
try:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            EmployeeID TEXT PRIMARY KEY,
            Name TEXT NOT NULL,
            DOB TEXT NOT NULL,
            Salary REAL NOT NULL,
            Department TEXT NOT NULL,
            JoinDate TEXT NOT NULL,
            Email TEXT,
            Age INTEGER,
            YearOfService INTEGER
        )
    """)

    # Insert rows (use INSERT OR REPLACE to avoid duplicate key errors)
    for _, row in df.iterrows():
        cursor.execute(f"""
            INSERT OR REPLACE INTO {TABLE_NAME} 
            (EmployeeID, Name, DOB, Salary, Department, JoinDate, Email, Age, YearOfService)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            str(row["EmployeeID"]),
            str(row["Name"]),
            str(row["DOB"].date()),  # store as string
            float(row["Salary"]),
            str(row["Department"]),
            str(row["JoinDate"].date()),  # store as string
            str(row["Email"]),
            int(row["Age"]),
            int(row["YearOfService"])
        ))

    conn.commit()
    print(f"Data successfully inserted into {DB_FILE} -> {TABLE_NAME}")
    conn.close()

except sqlite3.Error as e:
    print(f"SQLite error: {e}")
except Exception as e:
    print(f"Unexpected DB error: {e}")
