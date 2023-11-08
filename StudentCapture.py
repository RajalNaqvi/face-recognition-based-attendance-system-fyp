import cv2  

def StudentCapture(path,ip):
    cam = cv2.VideoCapture(ip)
    img_counter = 0
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("CAPTURING", frame)

        k = cv2.waitKey(1)
        if img_counter==10 or k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif  k%256 == 32:
            img_name =  path+"_{}.png".format(img_counter)
            print(img_name)
            print(type(img_name))
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1

    cam.release()
    cv2.destroyAllWindows()