import face_recognition as fr
import cv2
import numpy as np
import os
from img_encoder import known_name_encodings, known_names, collect_faces, load_data
import data_manager

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
    
    # image path
    img = path
    
    try: # read image with opencv
        image = cv2.imread(img)
    except:
        print("Can't read image from: ", path)
        return 
    
    # get face encodings an locations from image
    face_locations = fr.face_locations(image)
    face_encodings = fr.face_encodings(image, face_locations)

    # comparing and so on...
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = fr.compare_faces(known_name_encodings, face_encoding)
        name = ""

        face_distances = fr.face_distance(known_name_encodings, face_encoding)
        best_match = np.argmin(face_distances)
        
    #print("mathes: ", known_names)
    
    if matches[best_match]:
        print("Found: ", known_names[best_match])
    return known_names[best_match]

test = "faces\\mir.jpg"
datamanager = data_manager.DataManager('patients.db')
if __name__ == '__main__':
    patient = compare(test)
    print(datamanager.find_patient_by_name(patient))
