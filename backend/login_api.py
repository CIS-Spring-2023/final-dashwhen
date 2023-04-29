from flask import Flask, request, jsonify, Blueprint, session, redirect, url_for
import mysql.connector
from creds import Creds
from mysql.connector import Error
from sql import create_connection, execute_query, execute_read_query
import bcrypt

# Create a new Flask blueprint for the login API
login_api = Blueprint('login_api', __name__)

# Establish a connection to the MySQL server
for i in range(3):
    try:
        cnx = mysql.connector.connect(
            host=Creds.conString,
            user=Creds.userName,
            password=Creds.password,
            database=Creds.dbName
        )
        cursor = cnx.cursor(buffered=True)  
        break
    except Error as e:
        print(f"Error: {e}")
else:
    print("Failed to establish a connection to the MySQL server after 3 attempts.")

# User authentication routes
def login(username, password):
    # Validate the user's credentials against the user database
    query = "SELECT id, password FROM users WHERE username = %s"
    values = (username,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    if result is None:
        return True
    user_id, hashed_password = result
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
        return False
    else:
        return True