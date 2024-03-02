import cv2 as cv
import numpy as np
from umucv.stream import autoStream
from umucv.util import Video
from umucv.util import ROI, putText
import time

cv.namedWindow("input")
cv.moveWindow('input', 0, 0)
region = ROI("input")
video = Video(fps=15, codec="MJPG",ext="avi")
video.ON = False
i = 0
trozo = []
tiempo = 0
for key,frame in autoStream():
    
    if region.roi:
        [x1,y1,x2,y2] = region.roi
        trozo = frame[y1:y2+1, x1:x2+1]
        cv.rectangle(frame, (x1,y1), (x2,y2), color=(0,255,255), thickness=2)
        putText(frame, f'{x2-x1+1}x{y2-y1+1}', orig=(x1,y1-8))

        if not region.DOWN:
            gray = cv.cvtColor(trozo, cv.COLOR_BGR2GRAY)
            if i == 20:
                bgGray = gray
            if i > 20:
                dif = cv.absdiff(gray, bgGray)
                _, th = cv.threshold(dif, 40, 255, cv.THRESH_BINARY)
                cnts, _ = cv.findContours(th, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
                
                for c in cnts:
                    area = cv.contourArea(c)
                    if area > 9000:
                        video.ON = True
                        masked = trozo.copy()
                        masked[th==0] = 0
                        cv.imshow('object', masked)
                        video.write(masked, video.ON)
                        tiempo = time.time_ns()
                if ((time.time_ns()-tiempo)/ 1000000000) > 3:
                    video.ON = False

            i = i+1
    #video.write(trozo, video.ON)
    video.ON = False
    h,w,_ = frame.shape
    putText(frame, f'{w}x{h}')
    cv.imshow('input',frame)

cv.destroyAllWindows()
video.release()
    
