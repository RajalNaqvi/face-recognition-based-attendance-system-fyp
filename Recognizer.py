from threading import Thread
from scipy.spatial.distance import cosine
import mtcnn
from keras.models import load_model
import argparse
from Functions import *
import cv2

class Recognizer:
    def __init__(self,frame=None):
        self.frame = frame
        self.stopped = False

    def start(self):
        Thread(target=self.rec, args=()).start()
        print("REC STARTED")
        return self

    def rec(self):
        encoder_model = 'Dataset/model/facenet_keras.h5'
        encodings_path = 'Dataset/encodings/2017_SEC_A.pkl'
        face_detector = mtcnn.MTCNN()
        face_encoder = load_model(encoder_model)
        encoding_dict = load_pickle(encodings_path)
        recognition_t=0.5
        confidence_t=0.5
        required_size=(160, 160)
        while not self.stopped:
            self.frame_rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.results = face_detector.detect_faces(self.frame_rgb)
            print(len(self.results))
            for res in self.results:
                if res['confidence'] < confidence_t:
                    continue
                face, pt_1, pt_2 = get_face(self.frame_rgb, res['box'])
                encode = get_encode(face_encoder, face, required_size)
                encode = l2_normalizer.transform(encode.reshape(1, -1))[0]
                name = 'unknown'
                distance = float("inf")
                for db_name, db_encode in encoding_dict.items():
                    dist = cosine(db_encode, encode)
                    if dist < recognition_t and dist < distance:
                        name = db_name
                        Classroom_Backend.MarkinDatabase(name)
                        distance = dist
                if name == 'unknown':
                    cv2.rectangle(self.frame, pt_1, pt_2, (0, 0, 255), 2)
                    cv2.putText(fself.rame, name, pt_1, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
                else:
                    cv2.rectangle(self.frame, pt_1, pt_2, (0, 255, 0), 2)
                    cv2.putText(self.frame, name, (pt_1[0], pt_1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 200, 200), 2)
                
                frame = self.frame

    def stop(self):
        self.stopped = True  
