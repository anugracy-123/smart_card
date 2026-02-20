
from flask import Flask, render_template, request
import cv2
import face_recognition
import sqlite3
import uuid
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'faces'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS smartcard (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aadhaar TEXT,
    ration TEXT,
    licence TEXT,
    smartcard TEXT
)
""")
conn.commit()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        aadhaar = request.form["aadhaar"]
        ration = request.form["ration"]
        licence = request.form["licence"]
        file = request.files["face"]

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], "user.jpg")
        file.save(filepath)

        image = face_recognition.load_image_file(filepath)
        face_locations = face_recognition.face_locations(image)

        if len(face_locations) == 0:
            return render_template("index.html", msg="❌ Face detect aagala")

        smartcard = "SC-" + str(uuid.uuid4())[:8]

        cursor.execute("INSERT INTO smartcard (aadhaar, ration, licence, smartcard) VALUES (?,?,?,?)",
                       (aadhaar, ration, licence, smartcard))
        conn.commit()

        return render_template("index.html", msg="✅ Smart Card Created", card=smartcard)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
