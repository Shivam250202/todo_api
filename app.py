from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import errorcode
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)



def create_db_connection():
    try:
        cnx = mysql.connector.connect(
            host="localhost",  
            user="root", 
            password="root",  
            database="todo_app"  
        )
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Access denied. Please check your MySQL credentials.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: Database does not exist.")
        else:
            print(f"Error: {err}")
        return None


@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required.'}), 400

    cnx = create_db_connection()
    if not cnx:
        return jsonify({'error': 'Failed to connect to the database.'}), 500

    cursor = cnx.cursor()
    try:
        hashed_password = generate_password_hash(password)
        cursor.execute("INSERT INTO users (password, username) VALUES (%s, %s)", (hashed_password,username))
        cnx.commit()
        return jsonify({'message': 'Registration successful.'}), 201
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({'error': 'Failed to register.'}), 500
    finally:
        cursor.close()
        cnx.close()


@app.route('/api/login', methods=['POST','GET'])
def login():
    
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required.'}), 400

    cnx = create_db_connection()
    if not cnx:
        return jsonify({'error': 'Failed to connect to the database.'}), 500

    cursor = cnx.cursor()
    try:
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        print(result)

        if result is None or not check_password_hash(result[0], password):
            return jsonify({'error': 'Invalid username or password.'}), 401

        
        return jsonify({'success': "user logged in"}), 200
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({'error': 'Failed to login.'}), 500
    finally:
        cursor.close()
        cnx.close()


@app.route('/api/todo', methods=['POST'])
def create_todo():
    # Check the user's authentication token here
    # ...

    id = request.json.get("id")
    title = request.json.get('title')
    description = request.json.get('description')

    if not title:
        return jsonify({'error': 'Title is required.'}), 400

    cnx = create_db_connection()
    if not cnx:
        return jsonify({'error': 'Failed to connect to the database.'}), 500

    cursor = cnx.cursor()
    try:
        cursor.execute("INSERT INTO todo (title, description) VALUES (%s, %s)", (title, description))
        cnx.commit()
        return jsonify({'message': 'Todo created successfully.'}), 201
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({'error': 'Failed to create a todo.'}), 500
    finally:
        cursor.close()
        cnx.close()


@app.route('/api/todo/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    # Check the user's authentication token here
    # ...

    title = request.json.get('title')
    description = request.json.get('description')

    if not title:
        return jsonify({'error': 'Title is required.'}), 400

    cnx = create_db_connection()
    if not cnx:
        return jsonify({'error': 'Failed to connect to the database.'}), 500

    cursor = cnx.cursor()
    try:
        cursor.execute("UPDATE todo SET title = %s, description = %s WHERE id = %s", (title, description, todo_id))
        cnx.commit()
        return jsonify({'message': 'Todo updated successfully.'}), 200
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({'error': 'Failed to update the todo.'}), 500
    finally:
        cursor.close()
        cnx.close()


@app.route('/api/todo/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    # Check the user's authentication token here
    # ...

    cnx = create_db_connection()
    if not cnx:
        return jsonify({'error': 'Failed to connect to the database.'}), 500

    cursor = cnx.cursor()
    try:
        cursor.execute("DELETE FROM todo WHERE id = %s", (todo_id,))
        cnx.commit()
        return jsonify({'message': 'Todo deleted successfully.'}), 200
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({'error': 'Failed to delete the todo.'}), 500
    finally:
        cursor.close()
        cnx.close()


if __name__ == '__main__':
    app.run(debug=True)
