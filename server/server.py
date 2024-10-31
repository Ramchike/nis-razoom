from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor
from database import *

app = Flask(__name__)


# CRUD для таблицы States
@app.route('/states', methods=['GET'])
def get_states():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM States;")
    states = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(states)


@app.route('/states', methods=['POST'])
def create_state():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO States (title, type, harm_allowance) VALUES (%s, %s, %s) RETURNING id;",
        (data['title'], data['type'], data['harm_allowance'])
    )
    state_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'id': state_id, 'title': data['title']}), 201


@app.route('/states/<int:id>', methods=['PUT'])
def update_state(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE States SET title = %s, type = %s, harm_allowance = %s WHERE id = %s;",
        (data['title'], data['type'], data['harm_allowance'], id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'State updated'})


@app.route('/states/<int:id>', methods=['DELETE'])
def delete_state(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM States WHERE id = %s;", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'State deleted'})


# CRUD для таблицы Employees
@app.route('/employees', methods=['GET'])
def get_employees():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM Employees;")
    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(employees)


@app.route('/employees', methods=['POST'])
def create_employee():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Employees (state_id, rank_id, unstand_allowance_id) VALUES (%s, %s, %s) RETURNING id;",
        (data['state_id'], data['rank_id'], data['unstand_allowance_id'])
    )
    employee_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'id': employee_id}), 201


@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Employees SET state_id = %s, rank_id = %s, unstand_allowance_id = %s WHERE id = %s;",
        (data['state_id'], data['rank_id'], data['unstand_allowance_id'], id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Employee updated'})


@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Employees WHERE id = %s;", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Employee deleted'})


# Расчет зарплаты сотрудника
@app.route('/employees/<int:id>/salary', methods=['GET'])
def calculate_salary(id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        SELECT Ranks.salary AS base_salary,
               States.harm_allowance AS harm_allowance,
               unstand_allowance.percent AS unstand_percent
        FROM Employees
        JOIN Ranks ON Employees.rank_id = Ranks.id
        JOIN States ON Employees.state_id = States.id
        JOIN unstand_allowance ON Employees.unstand_allowance_id = unstand_allowance.id
        WHERE Employees.id = %s;
    """, (id,))

    result = cursor.fetchone()
    if result:
        base_salary = result['base_salary']
        harm_allowance = result['harm_allowance']
        unstand_percent = result['unstand_percent']

        gross_salary = base_salary * (1 + harm_allowance + unstand_percent)
        net_salary = gross_salary * 0.87  # Учет налога 13%

        cursor.close()
        conn.close()

        return jsonify({
            'employee_id': id,
            'gross_salary': gross_salary,
            'net_salary': net_salary
        })

    cursor.close()
    conn.close()
    return jsonify({'error': 'Employee not found'}), 404


if __name__ == '__main__':
    initialize_db()
    app.run(debug=True)
