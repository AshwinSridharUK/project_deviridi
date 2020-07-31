#Adapted for use on Rasbian
import cv2
import requests
import numpy as np
cap= cv2.VideoCapture(0) # 0 means camera 
ret, frame1 = cap.read()
ret, frame2 = cap.read()

while cap.isOpened():
    difference= cv2.absdiff(frame1,frame2)
    grey=cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    bblur= cv2.GaussianBlur(grey,(5,5),0)
    _, thresh= cv2.threshold(bblur, 20,255,cv2.THRESH_BINARY)
    dilated=cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour)< 700:
            continue
        cv2.rectangle(frame1, (x,y), (x+w, y+h), (0,255,0), 2)
        cv2.putText(frame1, "Status:{}".format('Movement'), (10,20), cv2.FONT_HERSHEY_COMPLEX,
                                                   1,(0,0,255),3)
	requests.get("ENTER HTTP HERE") #enter azure here 

    #cv2.drawContours(frame1,contours,-1,(0,255,0),2)
    cv2.imshow ("feed",frame1)
    frame1=frame2
    ret, frame2=cap.read()
    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
cap.release()
