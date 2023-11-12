from Image_recognition import ImageRecognition
from keras.models import load_model
import mtcnn

detector = mtcnn.MTCNN()
encoder = load_model(r'C:\Users\my pc\Downloads\FYP (2)\FYP\FYP\Dataset\model\facenet_keras.h5')
encodings_path = r"C:\Users\my pc\Downloads\FYP (2)\FYP\FYP\Dataset\encodings\2017_SEC_A.pkl"
image_recognizer = ImageRecognition(encoder_model=encoder,detector_model=detector,
                 encodings_path=encodings_path)

image, person, is_present = image_recognizer.recognize_image(input_image=r"C:\Users\my pc\Downloads\FYP (2)\FYP\FYP\Dataset\images\example_04.jpg",output_image_path=r"D:\MyWork\MyFYP\face-recognition-based-attendance-system-fyp\face_recognition\test.jpg")
print(person)