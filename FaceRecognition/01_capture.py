# # USAGE
# With default parameter of user/id 
#       python3 01_capture.py -n default_user
# OR specifying the dataset and user/id
#       python3 01_capture.py -i dataset -n default_user

## Acknowledgement
## This code is adapted from:
## https://www.hackster.io/mjrobot/real-time-face-recognition-an-end-to-end-project-a10826

# import the necessary packages
import cv2
import os
import argparse

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--name", required=True,
    help="The name/id of this person you are recording")
ap.add_argument("-i", "--dataset", default='dataset',
    help="path to input directory of faces + images")
args = vars(ap.parse_args())

# use name as folder name
name = args["name"]
folder = './dataset/{}'.format(name)

# Create a new folder for the new name
if not os.path.exists(folder):
    os.makedirs(folder)
    os.makedirs('{}/eye'.format(folder))
    os.makedirs('{}/face'.format(folder))
    os.makedirs('{}/smile'.format(folder))


# Start the camera
cam = cv2.VideoCapture(0)
# Set video width
cam.set(3, 640) 
# Set video height
cam.set(4, 480)
# Get the pre-built classifier that had been trained on 3 million faces 
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
smile_detector = cv2.CascadeClassifier('haarcascade_smile.xml')
eye_detector = cv2.CascadeClassifier('haarcascade_eye.xml')
# Create a window
cv2.namedWindow("Saving Images... (Press Escape to end)")

# Save up to 10 images
img_counter = 0

while img_counter < 15:
    ret, frame = cam.read()
    cv2.imshow("test", frame)
    if not ret:
        break
    k = cv2.waitKey(1)

    # if ESC is pressed, break loop
    if k%256 == 27:
        print("Escape hit, closing...")
        break
    # if SPACE is pressed, look for the face/s in the image and classify them
    elif k%256 == 32:
        # to minimize processing, change color to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        # smile = smile_detector.detectMultiScale(gray,0.5,2.5)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

            eyes = eye_detector.detectMultiScale(roi_gray,1.5,5)
            for(ex, ey, ew, eh) in eyes:
                crop_img = roi_color[ey: ey + eh, ex: ex + ew]
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
                img_name = "{}/{:04}.jpg".format('{}/eye'.format(folder),img_counter)
                cv2.imwrite(img_name, crop_img)
                print("{} written!".format(img_name))
                img_counter += 1

            smile = smile_detector.detectMultiScale(roi_gray,1.5,15)
            for (xx, yy, ww, hh) in smile:
                cv2.rectangle(roi_color, (xx, yy), (xx + ww, yy + hh), (0, 255, 0), 2)
                img_name = "{}/{:04}.jpg".format('{}/smile'.format(folder),img_counter)
                cv2.imwrite(img_name, frame[y:y+h, x:x+w])
                print("{} written!".format(img_name))
                img_counter += 1

            img_name = "{}/{:04}.jpg".format('{}/face'.format(folder),img_counter)
            cv2.imwrite(img_name, frame[y:y+h, x:x+w])
            print("{} written!".format(img_name))
            img_counter += 1
            
            # Automatically encode/train the system
            os.system("python3 02_encode.py")



            smile = smile_detector.detectMultiScale(roi_gray,1.5,15)
            for (xx, yy, ww, hh) in smile:
                cv2.rectangle(roi_color, (xx, yy), (xx + ww, yy + hh), (0, 255, 0), 2)
   
cam.release()
cv2.destroyAllWindows()