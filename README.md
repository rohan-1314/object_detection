# What is this project?
This is an object detection program. this is a security program 
which can be used if you leave your laptop in an unsafe place and if someone
opens your laptop their image will be captured and sent to your email
.


## How it works?
This project is made using python and opencv. the program 
first converts the image to grayscale and then compares the first frame it took
to all the frames it captures until it finds a difference between the frames.
Then further processing is done on that frame. The computer
creates a rectangle around most likely object it detected and sends 
the image to the user's given email.


## how to run the program?
1) clone the repository
2) Please use a gmail account with the program if you use outlook or any other
account the program will not be able to send an email to that account.
3) when you run the program, you will see a prompt to enter 
your email and another prompt where you have to enter 0
to use the main (integrated) camera or 1 to use a secondary camera.
4) when the program runs, please go out of your video frame
otherwise the program will identify you as background and not work properly. After it starts 
you can try coming in frame or to bring some object in the video frame.

