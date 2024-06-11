import face_recognition as fr
import cv2
import numpy as np
import os
from img_encoder import known_name_encodings, known_names

test_image = "C:/Users/MiR/Desktop/minipro/faces/ElonM.jpg"

image = cv2.imread(test_image)

face_locations = fr.face_locations(image)

face_encodings = fr.face_encodings(image, face_locations)

for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
   matches = fr.compare_faces(known_name_encodings, face_encoding)
   name = ""

   face_distances = fr.face_distance(known_name_encodings, face_encoding)
   best_match = np.argmin(face_distances)
   
   #print("mathes: ", known_names)
   
   if matches[best_match]:
    print(known_names[best_match])
