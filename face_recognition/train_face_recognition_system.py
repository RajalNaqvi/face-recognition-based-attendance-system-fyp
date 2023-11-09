import os
import numpy as np
import cv2
from Functions import get_person_face, get_encoding, save_pickle
from sklearn.preprocessing import Normalizer
import logging

class TrainFaceRecognitionSystem:
    """
    Class for training a face recognition system.

    Args:
    - encoder_model (str): Path to the pre-trained face encoder model.
    - image_dataset_path (str): Path to the directory containing the image dataset.
    - encodings_path (str): Path to save the generated encodings.
    - color_space (int, optional): Color space conversion flag (default: cv2.COLOR_BGR2RGB).
    - normalizer_str (str, optional): Normalization strategy (default: "l2").
    """
    
    def __init__(self, encoder_model,detector_model, image_dataset_path: str, encodings_path: str,
                 color_space=cv2.COLOR_BGR2RGB, normalizer_str: str = "l2") -> None:
        
        self.encoder_model = encoder_model
        self.image_dataset = image_dataset_path
        self.encodings_path = encodings_path
        self.detector_model = detector_model
        self.required_size = (160, 160)
        self.color_space = color_space
        self.normalizer = Normalizer(normalizer_str)
        logging.basicConfig(level=logging.INFO)

    def train(self) -> dict:
        """
        Train the face recognition model and generate encodings for each person in the dataset.

        Returns:
        - encoding_dict (dict): Dictionary containing person names as keys and corresponding encodings.
        
        """
        encoding_dict = dict()
        try:
            # iterate over the provided dataset, and encode them.
            for person_name in os.listdir(self.image_dataset):
                person_dir = os.path.join(self.image_dataset, person_name)
                encodes = []
                logging.info(f"Loading image dataset for user {person_name}")

                #  Load the images of dataset of a person and encode them.
                for image_name in os.listdir(person_dir):
                    image_path = os.path.join(person_dir, image_name)
                    loaded_image_bgr = cv2.imread(image_path)
                    image = cv2.cvtColor(loaded_image_bgr, self.color_space)
                    results = self.detector_model.detect_faces(image)
                    
                    # if face inside provided image then append it to list of encodings of person.
                    if results:
                        res = max(results, key=lambda b: b['box'][2] * b['box'][3])
                        person_face, _, _ = get_person_face(image, res['box'])
                        encode = get_encoding(self.encoder_model, person_face, self.required_size)
                        encodes.append(encode)
                        
                # if provided dataset of person contains face images. 
                if encodes:
                    encode = np.sum(encodes, axis=0)
                    encode = self.normalizer.transform(np.expand_dims(encode, axis=0))[0]
                    encoding_dict[person_name] = encode
                    logging.info(f"Model training for user {person_name} completed successfully...")
                else:
                    logging.info(f"Dataset for user {person_name} not found...")
            
            # saving the encodings of provided dataset.
            save_pickle(self.encodings_path, encoding_dict)
            logging.info("Model Training Completed successfully...")
            return encoding_dict

        except FileNotFoundError:
            logging.error("Image dataset directory not found.")
        except Exception as e:
            logging.error(f"An error occurred during training: {str(e)}")
