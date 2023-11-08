from scipy.spatial.distance import cosine
import numpy as np
import cv2
import mtcnn
import Classroom_Backend
from keras.models import load_model
import matplotlib.pyplot as plt
from Functions import get_face, plt_show, get_encode, load_pickle, l2_normalizer, Attendace

def imgr(imagefile):
    encoder_model = 'Dataset/model/facenet_keras.h5'
    test_res_path = "Dataset/results/"+imagefile[2]+".jpg"
    recognition_t = 0.3
    required_size = (160, 160)

    encoding_dict = load_pickle(imagefile[1])
    face_detector = mtcnn.MTCNN()
    face_encoder = load_model(encoder_model)
    img = cv2.imread(imagefile[0])

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face_detector.detect_faces(img_rgb)
    for res in results:
        face, pt_1, pt_2 = get_face(img_rgb, res['box'])
        cv2.imwrite('rec.jpg', face)
        encode = get_encode(face_encoder, face, required_size)
        encode = l2_normalizer.transform(np.expand_dims(encode, axis=0))[0]
        x1,y1 = pt_1
        x2,y2 = pt_2
        name = 'unknown'
        distance = float("inf")

        for db_name, db_encode in encoding_dict.items():
            dist = cosine(db_encode, encode)
            if dist < recognition_t and dist < distance:
                name = db_name
                distance = dist
                    
        if name == 'unknown':
            cv2.rectangle(img, pt_1, pt_2, (0, 0, 255), 2)
            cv2.putText(img, name, pt_1, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        else:
            cv2.rectangle(img, (x1,y1), (x2,y2), (0, 255, 0), 2)
            cv2.putText(img, name, (x1+6,y2-6), cv2.FONT_HERSHEY_COMPLEX , 1, (255, 255, 255), 2)

    cv2.imwrite(test_res_path, img)
    plt_show(img)