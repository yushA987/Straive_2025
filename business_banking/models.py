import sqlite3

DB_FILE = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# def init_db():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("DROP TABLE IF EXISTS users")
#     cursor.execute("""
#         CREATE TABLE users (
#             UserID TEXT PRIMARY KEY,
#             UserName TEXT NOT NULL,
#             Balance REAL NOT NULL,
#             PAN TEXT,
#             TAN TEXT,
#             AccountType TEXT NOT NULL CHECK (AccountType IN ('Savings', 'Current')),
#             Salary Int
#         )
#     """)
#     conn.commit()
#     conn.close()
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("""
        CREATE TABLE users (
            UserID TEXT PRIMARY KEY,
            UserName TEXT NOT NULL,
            Balance REAL NOT NULL,
            PAN TEXT,
            TAN TEXT,
            AccountType TEXT NOT NULL CHECK (AccountType IN ('Savings', 'Current')),
            Salary INT,
            Password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# def insert_user(user):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("""
#         INSERT OR REPLACE INTO users (UserID, UserName, Balance, PAN, TAN, AccountType, Salary)
#         VALUES (?, ?, ?, ?, ?, ?, ?)
#     """, (user['UserID'], user['UserName'], user['Balance'], user['PAN'], user['TAN'], user['AccountType'], user['Salary']))
#     conn.commit()
#     conn.close()
def insert_user(user):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO users (UserID, UserName, Balance, PAN, TAN, AccountType, Salary, Password)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user['UserID'], user['UserName'], user['Balance'], user['PAN'], user['TAN'],
        user['AccountType'], user['Salary'], user['Password']
    ))
    conn.commit()
    conn.close()

# def get_user_by_id(user_id):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM users WHERE UserID = ?", (user_id,))
#     user = cursor.fetchone()
#     conn.close()
#     return user
def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE UserID = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

# def get_user_by_credentials(user_id, password):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM users WHERE UserID = ? AND Password = ?", (user_id, password))
#     user = cursor.fetchone()
#     conn.close()
#     return user
def get_user_by_credentials(user_id, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE UserID = ? AND Password = ?", (user_id, password))
    user = cursor.fetchone()

    # Debug: Print the user row if found
    if user:
        print("User found:", dict(user))  # Converts sqlite3.Row to dict
    else:
        print("No user found with given credentials.")

    conn.close()
    return user


def get_user_by_name(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE UserName = ?", (name,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users


def update_pan_tan(user_id, pan=None, tan=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Build dynamic query parts
    updates = []
    params = []

    if pan is not None:
        updates.append("PAN = ?")
        params.append(pan)
    if tan is not None:
        updates.append("TAN = ?")
        params.append(tan)

    if not updates:
        return False  # nothing to update

    params.append(user_id)
    sql = f"UPDATE users SET {', '.join(updates)} WHERE UserID = ?"
    cursor.execute(sql, params)
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated

def delete_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE UserID = ?", (user_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted


