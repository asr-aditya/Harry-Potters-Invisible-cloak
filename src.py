#importing libraries
import cv2
import time
import numpy as np

#edit the output video using fourcc codec
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc,20.0,(640,480))

#reading video '0' for webcam else route to video can be given
cap = cv2.VideoCapture(0)

#allow the system to sleep for 3 sec before webcam starts (get away from frame to provide background image)
time.sleep(3)
count = 0
background = 0

#capturing the background
for i in range(60):
    temp,background = cap.read()
background = np.flip(background, axis=1)

#read real time frame from webcam
while(cap.isOpened()):
    temp, img = cap.read()
    if not temp:
        break
    count += 1
    img = np.flip(img, axis=1)

    #bgr to hsv coz bgr is more sensitive to light
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_range = np.array([0,120,50])
    higher_range = np.array([10,255,255])
    mask1 = cv2.inRange(hsv, lower_range, higher_range)

    lower_range = np.array([170,120,70])
    higher_range = np.array([180,255,255])
    mask2 = cv2.inRange(hsv, lower_range, higher_range)

    mask1 = mask1 + mask2

    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))

    #segmenting out cloth color
    mask2 = cv2.bitwise_not(mask1)

    ## Segment the red color part out of the frame using bitwise and with the inverted mask
    layer1 = cv2.bitwise_and(img, img, mask = mask2)

    ## Create image showing static background frame pixels only for the masked region
    layer2 = cv2.bitwise_and(background, background, mask = mask1)

    #output
    output = cv2.addWeighted(layer1,1,layer2,1,0)

    out.write(output)
    cv2.putText(output, "To stop press 'q'", (5,15), cv2.FONT_HERSHEY_SIMPLEX ,0.6 , (0,), 3)
    cv2.imshow("boom!! magic",output)
    
    k = cv2.waitKey(3) & 0xFF
    if k == ord('q') :
        self.calib_switch = False
        cv2.destroyAllWindows()

