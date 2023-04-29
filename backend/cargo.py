from flask import Flask, request, jsonify, Blueprint
import mysql.connector, binascii
from creds import Creds
from mysql.connector import Error
from sql import create_connection, execute_query, execute_read_query
from queries import queries
from login_api import login
from datetime import datetime

cargo_blueprint = Blueprint('cargo_blueprint', __name__)

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

# GET request - fetch a cargo by ID
@cargo_blueprint.route('/cargo', methods=['GET'])
def get_cargo():
    if(login(request.args.get('username'), request.args.get('password'))):
        return jsonify({'message': 'Invalid username or password'}), 401
    shipid = queries.spaceshipIdGetParam(cursor, request)
    if(shipid is not None):
        assert request.args['shipid'] == shipid
    query, values = queries.cargoGet(request)
    cursor.execute(query, values)
    rows = cursor.fetchall()
    result = {} 
    i = 0
    for row in rows:
        i+=1
        newrequest = {'spaceship_id': row[-1]}
        newquery, newvalues = queries.spaceshipGetJson(newrequest)
        cursor.execute(newquery, newvalues)
        newrows = cursor.fetchone()
        result.update({i: {'weight': float(row[1]), 'cargotype': row[2], 'departure': row[3], 'arrival': row[4], 'spaceshipname': newrows[1]}})
    return jsonify(result)

# POST request - create a new cargo
@cargo_blueprint.route('/cargo', methods=['POST'])
def create_cargo():
    cargo = request.get_json()
    if(login(cargo['username'], cargo['password'])):
        return jsonify({'message': 'Invalid username or password'}), 401
    shipid = queries.spaceshipIdGetJson(cursor, cargo)
    if(shipid is None):
        return jsonify({'message': 'Could not locate spaceship'}), 404
    cargo['shipid'] = shipid
    values = []
    values.append(cargo['shipid'])
    query = "SELECT maxweight FROM spaceship WHERE id = %s"
    cursor.execute(query, values)
    spaceship_max_weight = float(cursor.fetchone()[0])
    cursor.fetchall()
    query = "SELECT SUM(weight) FROM cargo WHERE shipid = %s"
    cursor.execute(query, values)
    cargo_total_weight = cursor.fetchone()[0]
    if(cargo_total_weight is None):
        cargo_total_weight = 0
    cursor.fetchall()
    if((float(cargo['weight']) + float(cargo_total_weight)) > spaceship_max_weight):
        return jsonify({'message': 'Cargo weight exceeds spaceship limits'}), 404
    query = queries.cargoInsert
    values = (cargo['weight'], cargo['cargotype'], cargo['departure'], cargo['arrival'], cargo['shipid'])
    cursor.execute(query, values)
    cnx.commit()
    return jsonify({'message': 'Cargo created successfully'}), 201

# PUT request - update an existing cargo
@cargo_blueprint.route('/cargo', methods=['PUT'])
def update_cargo():
    cargo = request.get_json()
    if(login(cargo['username'], cargo['password'])):
        return jsonify({'message': 'Invalid username or password'}), 401
    old_spaceship_id = queries.spaceshipIdGetJson(cursor, cargo, m = "old_")
    if(old_spaceship_id is None):
        return jsonify({'message': 'Could not locate old spaceship'}), 404
    new_spaceship_id = queries.spaceshipIdGetJson(cursor, cargo, m = "new_")
    if(new_spaceship_id is None):
        new_spaceship_id = old_spaceship_id
    if(cargo.get('new_weight') is None):
        cargo['new_weight'] = cargo['old_weight']
    cargo['new_shipid'] = new_spaceship_id
    
    arrival_obj = datetime.strptime(cargo['old_arrival'], '%a, %d %b %Y')
    cargo['old_arrival'] = arrival_obj.strftime('%Y-%m-%d')
    
    departure_obj = datetime.strptime(cargo['old_departure'], '%a, %d %b %Y')
    cargo['old_departure'] = departure_obj.strftime('%Y-%m-%d')

    values = []
    values.append(cargo['new_shipid'])
    query = "SELECT maxweight FROM spaceship WHERE id = %s"
    cursor.execute(query, values)
    spaceship_max_weight = float(cursor.fetchone()[0])
    cursor.fetchall()
    query = "SELECT SUM(weight) FROM cargo WHERE shipid = %s"
    cursor.execute(query, values)
    cargo_total_weight = float(cursor.fetchone()[0])
    if(cargo_total_weight is None):
        cargo_total_weight = 0
    cursor.fetchall()
    if((float(cargo['new_weight']) + cargo_total_weight) > spaceship_max_weight):
        return jsonify({'message': 'Cargo weight exceeds spaceship limits'}), 404
    query, values = queries.cargoUpdate(cargo)
    print(query, values)
    cursor.execute(query, values)
    cnx.commit()
    return jsonify({'message': 'Cargo updated successfully'})

# DELETE request - delete a cargo by ID
@cargo_blueprint.route('/cargo', methods=['DELETE'])
def delete_cargo():
    cargo = request.get_json()
    if(login(cargo['username'], cargo['password'])):
        return jsonify({'message': 'Invalid username or password'}), 401
    shipid = queries.spaceshipIdGetJson(cursor, cargo)
    if(shipid is not None):
        cargo['shipid'] = shipid
    
    arrival_obj = datetime.strptime(cargo['arrival'], '%a, %d %b %Y')
    cargo['arrival'] = arrival_obj.strftime('%Y-%m-%d')
    
    departure_obj = datetime.strptime(cargo['departure'], '%a, %d %b %Y')
    cargo['departure'] = departure_obj.strftime('%Y-%m-%d')

    query, values = queries.cargoDelete(cargo)
    cursor.execute(query, values)
    cnx.commit()
    return jsonify({'message': 'Cargo deleted successfully'})