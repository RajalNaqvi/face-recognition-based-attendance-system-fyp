import pickle
import numpy as np
import matplotlib.pyplot as plt
import Classroom_Backend
import cv2
from sklearn.preprocessing import Normalizer
from datetime import datetime
from scipy.spatial.distance import cosine
import os
from datetime import datetime

now = datetime.now()
TimeFirstSession = now.strftime("%H:%M:%S")
l2_normalizer = Normalizer('l2')

def Attendace(name):
    with open('Dataset/Attendance/Attendace.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            print("*************************************")
            print(f'{name},{dtString}' + " Attendace Marked")
            print("*************************************")
            f.writelines(f'\n{name},{dtString}')
def get_encode(face_encoder, face, size):
    face = normalize(face)
    face = cv2.resize(face, size)
    encode = face_encoder.predict(np.expand_dims(face, axis=0))[0]
    return encode
def get_face(img, box):
    x1, y1, width, height = box
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    face = img[y1:y2, x1:x2]
    return face, (x1, y1), (x2, y2)
def get_keypoints(img,keypoints):
    cv2.circle(img,(keypoints['left_eye']), 2, (100, 255, 0), 2)
    cv2.circle(img,(keypoints['right_eye']), 2, (100, 255, 0), 2)
    cv2.circle(img,(keypoints['nose']), 2, (100, 255, 0), 2)
    cv2.circle(img,(keypoints['mouth_left']), 2, (100, 255, 0), 2)
    cv2.circle(img,(keypoints['mouth_right']), 2, (100, 255, 0), 2)
    return img
def get_pic(img,code):
    for i in code:
        cv2.circle(img,(keypoints['left_eye']), 2, (100, 255, 0), 2)
        cv2.putText(img, i, pt_1, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
def normalize(img):
    mean, std = img.mean(), img.std()
    return (img - mean) / std
def recognize(img,
              detector,
              encoder,
              encoding_dict,
              recognition_t=0.5,
              confidence_t=0.50,
              required_size=(160, 160), ):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = detector.detect_faces(img_rgb)
    for res in results:
        if res['confidence'] < confidence_t:
            continue
        face, pt_1, pt_2 = get_face(img_rgb, res['box'])
        encode = get_encode(encoder, face, required_size)
        encode = l2_normalizer.transform(encode.reshape(1, -1))[0]
        name = 'unknown'
        print("TOTAL PERSON DETECTED = "+str(len(results)))

        distance = float("inf")
        for db_name, db_encode in encoding_dict.items():
            dist = cosine(db_encode, encode)
            if dist < recognition_t and dist < distance:
                name = db_name
                #Classroom_Backend.MarkinDatabase(name,data)
                distance = dist

        if name == 'unknown':
            cv2.rectangle(img, pt_1, pt_2, (0, 0, 255), 2)
            cv2.putText(img, name, pt_1, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
        else:
            cv2.rectangle(img, pt_1, pt_2, (0, 255, 0), 2)
            cv2.putText(img, name, (pt_1[0], pt_1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 200, 200), 2)
    return img
def plt_show(cv_img):
    img_rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    plt.imshow(img_rgb)
    plt.show()
def load_pickle(path):
    with open(path, 'rb') as f:
        encoding_dict = pickle.load(f)
    return encoding_dict
def save_pickle(path, obj):
    with open(path, 'wb') as file:
        pickle.dump(obj, file)