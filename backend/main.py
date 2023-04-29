import hashlib
from flask import Flask, request, jsonify
import mysql.connector
from creds import Creds
from mysql.connector import Error
from sql import create_connection, execute_query, execute_read_query
from captain import captain_blueprint
from spaceship import spaceship_blueprint
from cargo import cargo_blueprint

app = Flask(__name__)
app.config["DEBUG"] = True

app.register_blueprint(captain_blueprint)
app.register_blueprint(spaceship_blueprint)
app.register_blueprint(cargo_blueprint)

if __name__ == '__main__':
    app.run()