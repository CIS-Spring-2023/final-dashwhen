import binascii
from flask import Flask, request, jsonify, Blueprint
import mysql.connector
from creds import Creds
from mysql.connector import Error
from sql import create_connection, execute_query, execute_read_query
from queries import queries
from login_api import login

captain_blueprint = Blueprint('captain_blueprint', __name__)

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

# GET request - fetch a captain by ID
@captain_blueprint.route('/captain', methods=['GET'])
def get_captain():
    if(login(request.args.get('username'), request.args.get('password'))):
        return jsonify({'message': 'Invalid username or password'}), 401
    query, values = queries.captainGet(request)
    cursor.execute(query, values)
    rows = cursor.fetchall()
    result = {}
    i = 0
    for row in rows:
        i+=1
        result.update({i: {'firstname': row[1], 'lastname': row[2], 'captain_rank': row[3], 'homeplanet': row[4]}})
    return jsonify(result)

# POST request - create a new captain
@captain_blueprint.route('/captain', methods=['POST'])
def create_captain():
    captain = request.get_json()
    if(login(captain['username'], captain['password'])):    
        return jsonify({'message': 'Invalid username or password'}), 401
    query = queries.captainInsert
    values = (captain['firstname'], captain['lastname'], captain['captain_rank'], captain['homeplanet'])
    cursor.execute(query, values)
    cnx.commit()
    return jsonify({'message': 'Captain created successfully'}), 201

# PUT request - update an existing captain
@captain_blueprint.route('/captain', methods=['PUT'])
def update_captain():
    captain = request.get_json()
    if(login(captain['username'], captain['password'])):
        return jsonify({'message': 'Invalid username or password'}), 401
    query, values = queries.captainUpdate(request)
    cursor.execute(query, values)
    cnx.commit()
    return jsonify({'message': 'Captain(s) updated successfully'})

# DELETE request - delete a captain by ID
@captain_blueprint.route('/captain', methods=['DELETE'])
def delete_captain():
    captain = request.get_json()
    if(login(captain['username'], captain['password'])):
        return jsonify({'message': 'Invalid username or password'}), 401
    query, values = queries.captainDelete(request)
    cursor.execute(query, values)
    cnx.commit()
    return jsonify({'message': 'Captain(s) deleted successfully'})