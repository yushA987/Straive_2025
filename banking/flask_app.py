from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DB_FILE = "employees.db"
TABLE_NAME = "employees"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # for dict-like access
    return conn

@app.route('/employees', methods=['GET'])
def get_all_employees():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {TABLE_NAME}")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return jsonify({"message": "No data found"}), 404

        result = [dict(row) for row in rows]
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/employees/<emp_id>', methods=['GET'])
def get_employee(emp_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE EmployeeID = ?", (emp_id,))
        row = cursor.fetchone()
        conn.close()

        if row is None:
            return jsonify({"message": "Employee not found"}), 404

        return jsonify(dict(row)), 200

    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.get_json()

    required_fields = ["EmployeeID", "Name", "DOB", "Salary", "Department", "JoinDate"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(f"""
            INSERT INTO {TABLE_NAME}
            (EmployeeID, Name, DOB, Salary, Department, JoinDate, Email, Age, YearOfService)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("EmployeeID"),
            data.get("Name"),
            data.get("DOB"),
            float(data.get("Salary")),
            data.get("Department"),
            data.get("JoinDate"),
            data.get("Email"),
            int(data.get("Age", 0)),
            int(data.get("YearOfService", 0))
        ))

        conn.commit()
        conn.close()

        return jsonify({"message": "Employee added successfully"}), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "EmployeeID already exists"}), 409
    except Exception as e:
        return jsonify({"error": f"Failed to add employee: {str(e)}"}), 500


@app.route('/employees/<emp_id>', methods=['PUT'])
def update_employee(emp_id):
    data = request.get_json()

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE EmployeeID = ?", (emp_id,))
        if cursor.fetchone() is None:
            return jsonify({"message": "Employee not found"}), 404

        cursor.execute(f"""
            UPDATE {TABLE_NAME}
            SET Name = ?, DOB = ?, Salary = ?, Department = ?, JoinDate = ?, Email = ?, Age = ?, YearOfService = ?
            WHERE EmployeeID = ?
        """, (
            data.get("Name"),
            data.get("DOB"),
            float(data.get("Salary")),
            data.get("Department"),
            data.get("JoinDate"),
            data.get("Email"),
            int(data.get("Age", 0)),
            int(data.get("YearOfService", 0)),
            emp_id
        ))

        conn.commit()
        conn.close()

        return jsonify({"message": "Employee updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to update employee: {str(e)}"}), 500

@app.route('/employees/<emp_id>', methods=['DELETE'])
def delete_employee(emp_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE EmployeeID = ?", (emp_id,))
        conn.commit()
        conn.close()

        if cursor.rowcount == 0:
            return jsonify({"message": "Employee not found"}), 404

        return jsonify({"message": "Employee deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to delete employee: {str(e)}"}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Employee API is running"}), 200


if __name__ == '__main__':
    app.run(debug=True)
