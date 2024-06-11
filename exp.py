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
       name = known_names[best_match]

   cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
   cv2.rectangle(image, (left, bottom - 15), (right, bottom), (0, 0, 255), cv2.FILLED)

   font = cv2.FONT_HERSHEY_DUPLEX
   cv2.putText(image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

cv2.imshow("Result", image)
cv2.imwrite("./output.jpg", image)
cv2.waitKey(0)
cv2.destroyAllWindows()