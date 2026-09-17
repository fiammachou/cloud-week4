import os
from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "mysql"),
        user=os.getenv("DB_USER", "clouduser"),
        password=os.environ["DB_PASSWORD"],
        database=os.getenv("DB_NAME", "clouddb")
    )

@app.route("/")
def home():
    return "Backend is working"

@app.route("/status")
def status():
    return jsonify({"message": "Backend API is working"})

@app.route("/visits")
def visits():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("UPDATE visits SET count = count + 1 WHERE id = 1")
    connection.commit()

    cursor.execute("SELECT count FROM visits WHERE id = 1")
    count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return jsonify({"visits": count})
