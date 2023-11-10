import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
import cv2
from sklearn.preprocessing import Normalizer
from datetime import datetime
from keras.models import load_model

# Attendance[ This Method will be Replaced with dbloolup]
def attendance(name):
    """
    Mark attendance for a given person.

    Args:
    - name (str): Name of the person.

    Writes the attendance entry to 'Dataset/Attendance/Attendance.csv'.
    """
    with open('Dataset/Attendance/Attendance.csv', 'r+') as f:
        my_data_list = f.readlines()
        name_list = []
        for line in my_data_list:
            entry = line.split(',')
            name_list.append(entry[0])
        if name not in name_list:
            now = datetime.now()
            dt_string = now.strftime('%H:%M:%S')
            print("*************************************")
            print(f'{name},{dt_string}' + " Attendance Marked")
            print("*************************************")
            f.writelines(f'\n{name},{dt_string}')

# Get encoding
def get_encoding(face_encoder_model, person_face, size):
    """
    Get the encoding for a person's face.

    Args:
    - face_encoder_model: Face encoder model.
    - person_face: Face image of the person.
    - size (tuple): Required size for the face image.

    Returns:
    - encode: Face encoding.
    """
    face = normalize(person_face)
    face = cv2.resize(face, size)
    encode = face_encoder_model.predict(np.expand_dims(face, axis=0))[0]
    return encode

def get_person_face(img, box):
    """
    Get the face region from an image based on the detected bounding box.

    Args:
    - img: Input image.
    - box (tuple): Bounding box coordinates (x, y, width, height).

    Returns:
    - face: Cropped face region.
    - pt_1 (tuple): Top-left corner of the bounding box.
    - pt_2 (tuple): Bottom-right corner of the bounding box.
    """
    x1, y1, width, height = box
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    face = img[y1:y2, x1:x2]
    return face, (x1, y1), (x2, y2)

l2_normalizer = Normalizer('l2')

def initialize_model(encoder_model_path):
    """
    Initialize the face encoder model.

    Returns:
    - model: Loaded face encoder model.
    """
    encoder_model = load_model(encoder_model_path)
    return encoder_model

def normalize(img):
    """
    Normalize the pixel values of an image.

    Args:
    - img: Input image.

    Returns:
    - normalized_img: Normalized image.
    """
    mean, std = img.mean(), img.std()
    return (img - mean) / std

def plt_show(cv_img):
    """
    Display an image using Matplotlib.

    Args:
    - cv_img: Input image in OpenCV format.
    """
    img_rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    plt.imshow(img_rgb)
    plt.show()

def load_pickle(path):
    """
    Load a pickle file.

    Args:
    - path (str): Path to the pickle file.

    Returns:
    - obj: Loaded object from the pickle file.
    """
    with open(path, 'rb') as f:
        obj = pickle.load(f)
    return obj

def save_pickle(path, obj):
    """
    Save an object to a pickle file.

    Args:
    - path (str): Path to save the pickle file.
    - obj: Object to be saved.
    """
    with open(path, 'wb') as file:
        pickle.dump(obj, file)

def read_vc(vc, func_to_call, break_print=':(', show=False, win_name='', break_key='q', **kwargs):
    """
    Read frames from a video capture object and apply a specified function to each frame.

    Args:
    - vc: Video capture object.
    - func_to_call: Function to be applied to each frame.
    - break_print (str, optional): Message to print upon breaking the loop.
    - show (bool, optional): Whether to display frames.
    - win_name (str, optional): Name of the window if show is True.
    - break_key (str, optional): Key to break the loop.
    - **kwargs: Additional keyword arguments to pass to func_to_call.
    """
    while vc.isOpened():
        ret, frame = vc.read()
        if not ret:
            print(break_print)
            break
        res = func_to_call(frame, **kwargs)
        if res is not None:
            frame = res

        if show:
            cv2.imshow(win_name, frame)
        if cv2.waitKey(1) & 0xff == ord(break_key):
            break