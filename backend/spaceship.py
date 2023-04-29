from flask import Flask, request, jsonify, Blueprint
import mysql.connector, binascii
from creds import Creds
from mysql.connector import Error
from sql import create_connection, execute_query, execute_read_query
from queries import queries
from login_api import login

spaceship_blueprint = Blueprint('spaceship_blueprint', __name__)

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

# GET request - fetch a spaceship by ID
@spaceship_blueprint.route('/spaceship', methods=['GET'])
def get_spaceship():
    if(login(request.args.get('username'), request.args.get('password'))):
        return jsonify({'message': 'Invalid username or password'}), 401
    captainid = queries.captainIdGetParam(cursor, request)
    if(captainid is not None):
        assert request.args['captainid'] == captainid
    query, values = queries.spaceshipGet(request)
    cursor.execute(query, values)
    rows = cursor.fetchall()
    result = {}
    i = 0
    for row in rows:
        i+=1
        newrequest = {'id': row[-1]}
        newquery, newvalues = queries.captainGetJson(newrequest)
        cursor.execute(newquery, newvalues)
        newrows = cursor.fetchone()
        captainFullTitle = newrows[3] + " " + newrows[1] + " " + newrows[2] + " of " + newrows[4]
        result.update({i: {'name': row[1], 'maxweight': float(row[2]), 'captain': captainFullTitle}})
    return jsonify(result)

# POST request - create a new spaceship
@spaceship_blueprint.route('/spaceship', methods=['POST'])
def create_spaceship():
    spaceship = request.get_json()
    if(login(spaceship['username'], spaceship['password'])):
        return jsonify({'message': 'Invalid username or password'}), 401
    captainid = queries.captainIdGetJson(cursor, spaceship)
    if(captainid is None):
        return jsonify({'message': 'Could not locate captain'}), 404
    spaceship['captainid'] = captainid
    query = queries.spaceshipInsert
    values = (spaceship['name'], spaceship['maxweight'], spaceship['captainid'])
    cursor.execute(query, values)
    cnx.commit()
    return jsonify({'message': 'Spaceship created successfully'}), 201

# PUT request - update an existing spaceship
@spaceship_blueprint.route('/spaceship', methods=['PUT'])
def update_spaceship():
    spaceship = request.get_json()
    if(login(spaceship['username'], spaceship['password'])):
        return jsonify({'message': 'Invalid username or password'}), 401
    old_captainid = queries.captainIdGetJson(cursor, spaceship, n = "old_")
    new_captainid = queries.captainIdGetJson(cursor, spaceship, n = "new_")
    if(new_captainid is None):
        return jsonify({'message': 'Could not locate new captain'}), 404
    if(old_captainid is not None):
        spaceship['old_captainid'] = old_captainid
    spaceship['new_captainid'] = new_captainid
    query, values = queries.spaceshipUpdate(spaceship)
    cursor.execute(query, values)
    cnx.commit()
    return jsonify({'message': 'Spaceship updated successfully'})

# DELETE request - delete a spaceship by ID
@spaceship_blueprint.route('/spaceship', methods=['DELETE'])
def delete_spaceship():
    spaceship = request.get_json()
    if(login(spaceship['username'], spaceship['password'])):
        return jsonify({'message': 'Invalid username or password'}), 401
    captainid = queries.captainIdGetJson(cursor, spaceship)
    if(captainid is not None):
        spaceship['captainid'] = captainid
    query, values = queries.spaceshipDelete(spaceship)
    cursor.execute(query, values)
    cnx.commit()
    return jsonify({'message': 'Spaceship deleted successfully'})