from face_recognition import ImageRecognition, Functions, VideoBasedImageRecognition, RealTimeRecognition
from keras.models import load_model
import mtcnn
import logging

detector = mtcnn.MTCNN()
encoder = load_model('facenet_keras.h5')
encodings_path = r"C:\Users\my pc\Downloads\FYP (2)\FYP\FYP\Dataset\encodings\2017_SEC_A.pkl"

#Image Recogonition
image_recognizer = ImageRecognition(encoder_model=encoder,detector_model=detector,
                 encodings_path=encodings_path)

# image, person, is_present = image_recognizer.recognize_image(input_image=r"C:\Users\my pc\Downloads\FYP (2)\FYP\FYP\Dataset\images\example_04.jpg",output_image_path=r"D:\MyWork\MyFYP\face-recognition-based-attendance-system-fyp\face_recognition\test.jpg")
# logging.info(person)
# Functions.plt_show(image)


# Video Based Recognition
video_path = r'D:\MyWork\MyFYP\face-recognition-based-attendance-system-fyp\face_recognition\IMG_0479.MOV'
Functions.convert_video_avi(video_path,"testing")
video_test = VideoBasedImageRecognition(image_recognizer,
                                        video_path='testing.avi',
                                        video_output_path=r'D:\MyWork\MyFYP\face-recognition-based-attendance-system-fyp\face_recognition\IMG_04792.avi')
video_test.start_recognition()