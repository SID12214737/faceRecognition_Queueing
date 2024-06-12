import face_recognition as fr
import cv2
import numpy as np
import os
import json

Fpath = "faces/"
images = os.listdir(Fpath)

# Define the data file path
DATA_FILE = 'data_storage.json'

known_names = []
known_name_encodings = []

def save_data(known_names, known_name_encodings):
    """
    Save the known names and their corresponding encodings to a JSON file.
    The encodings are converted to lists to be JSON serializable.
    """
    # Convert the NumPy arrays to lists
    known_name_encodings_list = [encoding.tolist() for encoding in known_name_encodings]
    
    # Create the data dictionary
    data = {
        "known_names": known_names,
        "known_name_encodings": known_name_encodings_list
    }

    # Save the data to the JSON file
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def load_data():
    """
    Load the known names and their corresponding encodings from a JSON file.
    The encodings are converted back to NumPy arrays.
    """
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            # Convert lists back to NumPy arrays
            known_names = data["known_names"]
            known_name_encodings = [np.array(encoding) for encoding in data["known_name_encodings"]]
            return known_names, known_name_encodings
    return [], []

def collect_single_face(path):
    image = fr.load_image_file(path)
    image_path = path
    encoding = fr.face_encodings(image)[0]
    known_name_encodings.append(encoding)
    known_names.append(os.path.splitext(os.path.basename(image_path))[0].capitalize())   
    save_data(known_names, known_name_encodings)
    if fr.face_locations(image):
        return True
    return False


def collect_faces():
    for _ in images:
        collect_single_face(Fpath+_)
    
    if known_names:
        return True
    return False

if __name__ == "__main__":
    collect_faces()