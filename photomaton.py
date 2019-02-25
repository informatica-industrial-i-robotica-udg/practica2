import numpy as np
import cv2

imgNumber = 0
while(imgNumber < 10):
    cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop)
    ret,frame = cap.read() # return a single frame in variable `frame`
    cv2.imshow('img1',frame) #display the captured image
    if cv2.waitKey(0) & 0xFF == ord('y'): #save on pressing 'y'
        cv2.imwrite('left-img'+ str(imgNumber) +'.jpg',frame)
    imgNumber=imgNumber+1

cv2.destroyAllWindows()

cap.release()
