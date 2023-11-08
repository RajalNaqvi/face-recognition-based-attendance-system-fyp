import cv2  

def Start(ip):
    cam = cv2.VideoCapture(ip)
    img_counter = 0
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("Live Streaing", frame)
        k = cv2.waitKey(1)
        if img_counter==10 or k%256 == 27:
            print("Escape hit, closing...")
            break

    cam.release()
    cv2.destroyAllWindows()