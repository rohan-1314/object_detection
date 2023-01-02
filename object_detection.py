import cv2
import time
from send_email import send_email
import glob
import os
from threading import Thread

# take user input email and choice of camera
user_email = input('enter your email: ')
user_camera_input = int(input('please enter 0 to use main camera or 1 to use secondary camera: '))
# create video instance
video = cv2.VideoCapture(user_camera_input)
time.sleep(1)
first_frame = None
status_list = []
count = 1


# create clean images folder function
def clean_folder():
    images = glob.glob('images/*.png')
    for image in images:
        os.remove(image)
    print('folder cleaned')


try:
    while True:

        status = 0
        check, frame = video.read()
        # convert inage to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # add gaussian blur
        gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)
        # create first frame
        if first_frame is None:
            first_frame = gray_frame_gau
        # check difference between first and all frames
        delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
        # create threshold frame
        thresh_frame = cv2.threshold(delta_frame, 80, 255, cv2.THRESH_BINARY)[1]
        # create dilated frame
        dil_frame = cv2.dilate(thresh_frame, None, iterations=3)
        # create contours
        contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # create contour parameter
        for contour in contours:
            if cv2.contourArea(contour) < 5000:
                continue
            # get x,y coordinates and width and height
            x, y, w, h = cv2.boundingRect(contour)
            # create rectangle around object
            rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            # get most likely image to contain a good picture of the object
            if rectangle.any():
                status = 1
                cv2.imwrite(f'images/{count}.png', frame)
                count += 1
                all_images = glob.glob('images/*.png')
                index = int(len(all_images) / 2)
                image_with_object = all_images[index]
        # create checkpoint to send email
        status_list.append(status)
        status_list = status_list[-2:]
        if status_list[0] == 1 and status_list[1] == 0:
            # create email thread
            email_thread = Thread(target=send_email, args=(image_with_object, user_email))
            email_thread.daemon = True

            email_thread.start()
        # show the video
        cv2.imshow('Video', frame)
        # create quit function
        key = cv2.waitKey(1)
        if key == ord('q') or key == ord('Q'):
            # create clean image folder threading
            clean_thread = Thread(target=clean_folder)
            clean_thread.daemon = True
            clean_thread.start()
            break
# handle index error
except IndexError:
    print('please create an images folder in the same directory in which this file is.')
video.release()
