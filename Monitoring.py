import argparse
import cv2
from scipy.spatial.distance import cosine
import mtcnn
from keras.models import load_model
import Classroom_Backend
from VideoGet import VideoGet
from VideoShow import VideoShow
from Functions import *
import schedule
from datetime import date, timedelta, datetime
import time
import urllib.request

def Control(data):
    if data >= 1 and data <= 3:
        urllib.request.urlopen("http://192.168.0.100/action_page?code=Case1")
    elif data >= 4 and data <=6:
        urllib.request.urlopen("http://192.168.0.100/action_page?code=Case2")
    elif data >= 7:
        urllib.request.urlopen("http://192.168.0.100/action_page?code=Case3")
    return data
def Start(source):
    encoder_model = 'Dataset/model/facenet_keras.h5'
    face_detector = mtcnn.MTCNN()
    face_encoder = load_model(encoder_model)
    TIMEFMT = "%I:%M:%p"
    video_getter = VideoGet(source).start()
    video_shower = VideoShow(video_getter.frame).start()    
    while True:
        if video_getter.stopped or video_shower.stopped:
            video_shower.stop()
            video_getter.stop()
            break   
        TimeNow = datetime.now().strftime(TIMEFMT)
        fst = TimeNow[0:1]
        if fst=="0":
            TimeNow = TimeNow[1:8]
        else:
            TimeNow = TimeNow
        day = datetime.now().strftime("%A") 
        x = Classroom_Backend.SearchClass(day,TimeNow)
    
        if not x:
            #urllib.request.urlopen("http://192.168.0.100/action_page?code=Case0")
            image = video_getter.frame
            img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = face_detector.detect_faces(img_rgb)
            video_shower.frame = image
            continue
        else:
            stopped = True 
            encodings_path = str(x[10])

            EndTime = str(x[3])
            StartTime = str(x[2])
            TimeNow = datetime.now()
            DateToday = TimeNow.strftime("%Y-%m-%d ")

            data = (x[1],x[4],x[5],x[6] ,x[7],x[8],x[9])
            recognition_t=0.45
            confidence_t=0.4
            required_size=(160, 160)
            l2_normalizer = Normalizer('l2')

            while stopped:
                TimeNow = datetime.now().strftime(TIMEFMT)
                fst = TimeNow[0:1]
                if fst=="0":
                    TimeNow = TimeNow[1:8]
                else:
                    TimeNow = TimeNow
                EndTime = str(x[3])
                StartTime = str(x[2])
                image = video_getter.frame
                img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                StartTime= datetime.strptime(DateToday+StartTime,'%Y-%m-%d %I:%M:%p')
                End = datetime.strptime(DateToday+EndTime, '%Y-%m-%d %I:%M:%p')
                
                Sum = End - StartTime
                Sum = Sum.total_seconds()/60
                SSSDiff = (Sum)*3/4
                FSSDiff = (Sum)*1/4
                Time = datetime.now()
                TimeDiff = Time - StartTime
                TimeDiff = TimeDiff.total_seconds()/60
                results = face_detector.detect_faces(img_rgb)
                people = len(results)
                #Control(people)
                encoding_dict = load_pickle(encodings_path)

                for res in results:
                    if res['confidence'] < confidence_t:
                        continue
                    face, pt_1, pt_2 = get_face(img_rgb, res['box'])
                    encode = get_encode(face_encoder, face, required_size)
                    encode = l2_normalizer.transform(encode.reshape(1, -1))[0]
                    name = 'unknown'
                    distance = float("inf")

                    for db_name, db_encode in encoding_dict.items():
                        dist = cosine(db_encode, encode)
                        if dist < recognition_t and dist < distance:
                            name = db_name
                            if TimeDiff <= FSSDiff :
                                Classroom_Backend.MarkinDatabase(name,data)
                            if TimeDiff >= SSSDiff:
                                Classroom_Backend.MarkSecondSession(name,data)
                            distance = dist

                    if name == 'unknown':
                        cv2.rectangle(image, pt_1, pt_2, (0, 0, 255), 2)
                        cv2.putText(image, name, pt_1, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
                    else:
                            cv2.rectangle(image, pt_1, pt_2, (0, 255, 0), 2)
                            cv2.putText(image, name, (pt_1[0], pt_1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                        (0, 200, 200), 2)    
                video_shower.frame = image

                if TimeNow == EndTime:
                    break

#soruce = "rtsp://admin:hrmis1234@192.168.0.110:554/Streaming/Channels/101/"
soruce = "http://192.168.0.100:4747/video"
Start(soruce)
