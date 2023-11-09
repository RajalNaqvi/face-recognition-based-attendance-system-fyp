from scipy.spatial.distance import cosine
import numpy as np
import cv2
from Functions import get_person_face, get_encoding, load_pickle, attendance
from sklearn.preprocessing import Normalizer
import logging


class ImageRecognition:
    """
    Class for recognizing faces in an image.

    Args:
    - encoder_model (str): Path to the pre-trained face encoder model.
    - detector_model: Face detection model.
    - encodings_path (str): Path to the encodings file.
    - color_space (int, optional): Color space conversion flag (default: cv2.COLOR_BGR2RGB).
    - normalizer_str (str, optional): Normalization strategy (default: "l2").
    """
    def __init__(self, encoder_model, detector_model, encodings_path: str,
                 color_space=cv2.COLOR_BGR2RGB, normalizer: str = "l2") -> None:
        
        self.encoder_model = encoder_model
        self.encodings_path = encodings_path
        self.detector_model = detector_model
        self.required_size = (160, 160)
        self.color_space = color_space
        self.normalizer = Normalizer(normalizer)
        logging.basicConfig(level=logging.INFO)

    def recognize_image(self, input_image, output_image_path: str = None, 
                        recognition_threshold: float = 0.3, confidence_threshold: float = 0.50,
                        mark_attendance: bool = False) -> tuple:
        """
        Recognize faces in an image and optionally mark attendance.

        Args:
        - input_image (str or cv2.imread): Path to the input image.
        - output_image_path (str, optional): Path to save the output image with bounding boxes.
        - recognition_threshold (float, optional): Recognition threshold.
        - mark_attendance (bool, optional): Whether to mark attendance.

        Returns:
        - Tuple containing:
          - input_image: Input image in OpenCV format.
          - person_name (str): Recognized person's name.
          - is_present (str): Attendance status (marked or None).
        """
        try:
            encoding_dict = load_pickle(self.encodings_path)
            
            # load the image and detect face inside the image
            if isinstance(input_image,str):
                input_image = cv2.imread(input_image)
            image_colorspace_converted = cv2.cvtColor(input_image, self.color_space)
            results = self.detector_model.detect_faces(image_colorspace_converted)
            logging.info("Image Recognition in progress...")
            
            for res in results:
                if res['confidence'] < confidence_threshold:
                    continue
                person_face, pt_1, pt_2 = get_person_face(image_colorspace_converted, res['box'])
                encode = get_encoding(self.encoder_model, person_face, self.required_size)
                normalize_encode = self.normalizer.transform(np.expand_dims(encode, axis=0))[0]
                x1, y1 = pt_1
                x2, y2 = pt_2
                person_name = 'unknown'
                distance = float("inf")
                
                # measure the distance between the provided image encoding and stored encoding 
                for db_name, db_encode in encoding_dict.items():
                    dist = cosine(db_encode, normalize_encode)
                    person_name = db_name if (dist < recognition_threshold and dist < distance) else person_name
                
                # this attendance mechanism will be updated in the future which can write attendance provided db or csv
                is_present = attendance(person_name) if (mark_attendance and person_name != 'unknown') else None
                
                if person_name == 'unknown':
                    cv2.rectangle(input_image, pt_1, pt_2, (0, 0, 255), 2)
                    cv2.putText(input_image, person_name, pt_1, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

                else:
                    cv2.rectangle(input_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(input_image, person_name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    
                # writing recognized image on provided path   
                if output_image_path:
                    logging.info(f"writing output image {output_image_path}")
                    cv2.imwrite(output_image_path, input_image)
                    
            logging.info("Image Recognition completed successfully..")
            return input_image, person_name, is_present
        
        except FileNotFoundError:
            logging.error("Image File Not found.")
        except Exception as e:
            logging.error(f"An error occurred during recognition: {str(e)}")