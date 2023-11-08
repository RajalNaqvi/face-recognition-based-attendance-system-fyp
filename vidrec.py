import mtcnn
from keras.models import load_model
from Functions import *

def start(VideoFile):
    encoder_model = 'Dataset/model/facenet_keras.h5'
    face_detector = mtcnn.MTCNN()
    face_encoder = load_model(encoder_model)
    encoding_dict = load_pickle(VideoFile[1])
    stream = cv2.VideoCapture(VideoFile[0])
    frame_width = 640
    frame_height = 480
    out = cv2.VideoWriter("Dataset/results/"+VideoFile[2]+".avi",cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width,frame_height))
    print("processing...")
    width = 640
    height = 480
    dim = (width, height)
    while True:
        (ret, img) = stream.read()
        if not ret:
            break
        img = recognize(img, face_detector,face_encoder, encoding_dict)
        frame = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        out.write(frame)
        cv2.imshow('Video File', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
         break

    stream.release()
    out.release()
    cv2.destroyAllWindows()