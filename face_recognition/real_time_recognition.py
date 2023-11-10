from face_recognition import ImageRecognition
from threading import Thread
import cv2
from datetime import datetime
from face_recognition import dblookup
import logging

class VideoShow:
    def __init__(self, frame = None, dim: tuple = (640, 480)) -> None:
        self.frame = frame
        self.stopped = False
        self.dim = dim
        
    def start(self):
        Thread(target=self.show, args=()).start()
        return self

    def show(self):
        while not self.stopped:
            self.frame = cv2.resize(self.frame, self.dim, interpolation = cv2.INTER_AREA)
            cv2.imshow("RealTime Streaming", self.frame)
            if cv2.waitKey(1) == ord("q"):
                self.stopped = True

    def stop(self):
        self.stopped = True


class VideoGet:
    def __init__(self, src: str, dim: tuple = (640, 480)):
        self.stream = cv2.VideoCapture(src)
        self.dim = dim
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
        
    def start(self):    
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()
                dim = (640, 480)
                frame = cv2.resize(self.frame, dim, interpolation = cv2.INTER_AREA)

    def stop(self):
        self.stopped = True
    

class RealTimeRecognition:
    
    def __init__(self,image_recognizer: ImageRecognition, camera_src:str, is_class_schedule: bool = False) -> None:
        """
        Initializes the RealTimeRecognition class.

        Args:
        - image_recognizer: Instance of the ImageRecognition class.
        - camera_src: Source for the camera feed.
        - is_class_schedule: Boolean flag to indicate if there's a class schedule.
        """
        
        self.image_recognizer = image_recognizer
        self.camera_src = camera_src
        self.is_class_schedule = is_class_schedule
        
    def start_realtime_recognition(self):
        """
        Starts the real-time recognition process.
        """
        try:
            video_getter = VideoGet(self.camera_src).start()
            video_shower = VideoShow(video_getter.frame).start()    
            
            while True:
                if video_getter.stopped or video_shower.stopped:
                    video_shower.stop()
                    video_getter.stop()
                    break
                
                if self.is_class_schedule:
                    # Display only during class schedule
                    video_shower.frame = video_getter.frame
                    time_now = datetime.now().strftime("%I:%M:%p")
                    day = datetime.now().strftime("%A")
                    
                    try:
                        # Search for the class schedule
                        is_class_now, end_time = dblookup.search_class(day, time_now)
                    except Exception as db_error:
                        # Handle database lookup errors and log the exception
                        logging.exception(f"Database lookup error: {db_error}")
                        break
                    
                    if is_class_now is False:
                        continue
                    else:
                        # Recognize and display image during class
                        while is_class_now: 
                            time_now = datetime.now().strftime("%I:%M:%p")
                            try:
                                image = video_getter.frame
                                image, _, _ = self.image_recognizer.recognize_image(image, mark_attendance=True)
                                video_shower.frame = image
                                
                            except Exception as recognition_error:
                                # Handle image recognition errors
                                print(f"Recognition error: {recognition_error}")
                                
                            if time_now == end_time:
                                break
                                
                else:
                    while True:
                        # Recognize and display image without schedule constraints
                        image = video_getter.frame
                        image, _, _ = self.image_recognizer.recognize_image(image)
                        video_shower.frame = image
                        
                        # Break the loop if 'q' key is pressed
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                            
        except Exception as e:
            # Catch-all for any other unexpected exceptions
            print(f"Exception occurred: {e}")