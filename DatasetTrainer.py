import os
import pickle
import numpy as np
import cv2
import mtcnn
import matplotlib.pyplot as plt
from keras.models import load_model
from Functions import get_face, get_encode, l2_normalizer, normalize ,get_keypoints


def start(path):
    encoder_model = 'Dataset/model/facenet_keras.h5'
    required_size = (160, 160)
    face_detector = mtcnn.MTCNN()
    face_encoder = load_model(encoder_model)
    encoding_dict = dict()
    for person_name in os.listdir(path[0]):
        person_dir = os.path.join(path[0], person_name)
        encodes = []
        for img_name in os.listdir(person_dir):
            img_path = os.path.join(person_dir, img_name)
            img = cv2.imread(img_path)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = face_detector.detect_faces(img_rgb)
            if results:
                res = max(results, key=lambda b: b['box'][2] * b['box'][3])
                face, pt1, pt2 = get_face(img_rgb, res['box'])
                face = normalize(face)
                face = cv2.resize(face, required_size)
                encode = face_encoder.predict(np.expand_dims(face, axis=0))[0]
                encodes.append(encode)
        if encodes:
            encode = np.sum(encodes, axis=0)
            encode = l2_normalizer.transform(np.expand_dims(encode, axis=0))[0]
            encoding_dict[person_name] = encode

    for key in encoding_dict.keys():
        print(key)
        
    with open(path[1], 'bw') as file:
        pickle.dump(encoding_dict, file)
    print ("-----  DATASET TRAINED SUCCESSFULLY  ----- ")