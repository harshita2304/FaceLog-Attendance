import cv2
import mysql.connector
import numpy as np
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword",
    database="attendance_system"
)
cursor = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    # Capture image from webcam
    # Process the image for face recognition
    # Recognize the face and get student ID
    # Return response
    return jsonify({'message': 'Image captured and attendance marked successfully.'})

if __name__ == '__main__':
    app.run(debug=True)
