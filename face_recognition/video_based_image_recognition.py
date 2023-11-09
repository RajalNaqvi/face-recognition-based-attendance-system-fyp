import cv2
from Functions import *
import logging
from face_recognition import ImageRecognition

class VideoBasedImageRecognition:
    def __init__(self, image_recognizer: ImageRecognition,
                 video_path: str, video_output_path: str = None, 
                 frame_size: tuple = (640, 480)) -> None:
        """
        Initialize VideoBasedImageRecognition object.

        Parameters:
        - image_recognizer (ImageRecognition): An instance of the ImageRecognition class.
        - video_path (str): Path to the input video file.
        - video_output_path (str, optional): Path to the output video file. Defaults to None.
        - frame_size (tuple, optional): Size of the output frames. Defaults to (640, 480).
        """
        self.video_path = video_path
        self.frame_size = frame_size
        self.video_output_path = video_output_path
        self.image_recognizer = image_recognizer

        logging.basicConfig(level=logging.INFO)
    
    def start_recognition(self):
        """
        Start the video-based image recognition process.

        Returns:
        - str: A message indicating the completion of video recognition.
        """
        video_stream = cv2.VideoCapture(self.video_path)
        if self.video_output_path:
            out = cv2.VideoWriter(self.video_output_path,
                                  cv2.VideoWriter_fourcc('M','J','P','G'), 
                                  30, self.frame_size)
        
        while True:
            # Read a frame from the video stream
            (ret, image) = video_stream.read()
            
            # Break if the video stream is empty
            if not ret:
                break
            
            # Perform image recognition using the provided recognizer
            image, _, _ = self.image_recognizer(image)
            frame = cv2.resize(image, self.frame_size, interpolation=cv2.INTER_AREA)
            
            # Write frame to output video if specified
            if self.video_output_path:
                out.write(frame)
            
            # Display the frame
            cv2.imshow('Video File', frame)
            
            # Break the loop if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Release video stream and output video
        video_stream.release()
        release_output = None if (self.video_output_path is None) else out.release()
        
        # Close all OpenCV windows
        cv2.destroyAllWindows()
        
        return f"Video recognition complete. Output file is at {self.video_path}."