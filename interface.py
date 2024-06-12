from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import base64
from queue import Queue
import face_recognition as fr
import cv2
import numpy as np
from img_encoder import known_name_encodings, known_names, collect_faces, load_data
from data_manager import DataManager
import threading

patients_queue = Queue()
lock = threading.Lock()

known_names, known_name_encodings = load_data()
if not (known_name_encodings and known_names):
    print("No known faces in the list!!!.")
    print("Collecting lists...")
    collect_faces()
    print("NOTE: ", len(known_names), " faces added to the list.\n")
    known_names, known_name_encodings = load_data()
    if not (known_name_encodings and known_names):
        print("WARNING: DATABASE EMPTY")


def compare(path):    
    try: # read image with opencv
        image = cv2.imread(path)
    except:
        print("Can't read image from: ", path)
        return 
    
    # get face encodings an locations from image
    face_locations = fr.face_locations(image)
    face_encodings = fr.face_encodings(image, face_locations)

    # initializing matches to an empty list
    matches = []

    # comparing and so on...
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = fr.compare_faces(known_name_encodings, face_encoding)
        name = ""

        face_distances = fr.face_distance(known_name_encodings, face_encoding)
        best_match = np.argmin(face_distances)
        
    #print("mathes: ", known_names)
    matched_name = None
    if matches and matches[best_match]:
        matched_name = known_names[best_match]
        print("Found: ", matched_name)
    return matched_name

def add_to_queue(patient):
    dataManager = DataManager('patients.db')  # Create DataManager instance within each request
    _ = dataManager.find_patient_by_name(patient)
    print(_)
    if len(_) != 0:
        if patient not in patients_queue.queue:
            patients_queue.put(_)
            return f"{patient} successfully added to the queue"
        else:
            return f"{patient} is already in the queue"
    else:
        return "Patient can't be found from database!"


def dequeue_patient():
    with lock:
        if not patients_queue.empty():
            return patients_queue.get()
        else:
            return "Queue is empty"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Dummy data storage
data_storage = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        text_input = request.form['text_input']
        image_file = request.files['image_file']
        if image_file:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
            image_file.save(image_path)
            data_storage.append({'text': text_input, 'image': image_file.filename})
            return redirect(url_for('confirmation'))
    return render_template('register.html')

@app.route('/register_live', methods=['GET', 'POST'])
def register_live():
    if request.method == 'POST':
        text_input = request.form['text_input']
        image_data = request.form['image_data']
        if image_data:
            # Decode the base64 image data
            image_data = image_data.split(",")[1]
            image_data = base64.b64decode(image_data)
            image_filename = f"{text_input.replace(' ', '_')}.png"
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            with open(image_path, 'wb') as f:
                f.write(image_data)
            data_storage.append({'text': text_input, 'image': image_filename})
            return redirect(url_for('confirmation'))
    return render_template('register_live.html')

@app.route('/queue_live', methods=['GET', 'POST'])
def queue_live():
    if request.method == 'POST':
        image_data = request.form['image_data']
        if image_data:
            # Decode the base64 image data
            image_data = image_data.split(",")[1]
            image_data = base64.b64decode(image_data)
            image_filename = f"queued_image_{len(data_storage) + 1}.png"
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            
            with open(image_path, 'wb') as f:
                f.write(image_data)
            
            persona = compare(image_path)
            if(persona):

                message = add_to_queue(persona) 
            else:
                message = "Face is not recognized"

            # Simulate some processing and return a response
            response = {"message": message}
            return jsonify(response)
    return render_template('queue_live.html')

@app.route('/queue', methods=['GET', 'POST'])
def queue():
    if request.method == 'POST':
        image_file = request.files['image_file']
        if image_file:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
            image_file.save(image_path)
            persona = compare(image_path)

            if(persona):
                message = add_to_queue(persona)  
            else:
                message = "Face is not recognized"

            # Simulate some processing and return a response
            response = {"message": message}
            return render_template('queue.html', response=response)
    return render_template('queue.html', response=None)

@app.route('/confirmation')
def confirmation():
    return "Registration successful!"

@app.route('/data')
def data():
    queue_contents = list(patients_queue.queue)
    return render_template('data.html', queue_contents=queue_contents)

@app.route('/dequeue', methods=['POST'])
def dequeue():
    patient = dequeue_patient()
    return redirect('/data')

if __name__ == '__main__':
    app.run(debug=True)
