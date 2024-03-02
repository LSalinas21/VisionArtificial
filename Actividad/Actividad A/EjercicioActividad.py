#!/usr/bin/env python

# ejemplo de selección de ROI

import numpy as np
import cv2 as cv
import time

from umucv.util import ROI, putText
from umucv.stream import autoStream
from umucv.util import Video



cv.namedWindow("input")
cv.moveWindow('input', 0, 0)

region = ROI("input")
rectangulo = False
video = Video(fps=15, codec="MJPG",ext="avi")
trozo = []
bgsub = cv.createBackgroundSubtractorMOG2(500, 16, False)
video.ON = False
tiempo = 0

for key, frame in autoStream():

    if region.roi:
        [x1,y1,x2,y2] = region.roi
        trozo = frame[y1:y2+1, x1:x2+1]

        cv.rectangle(frame, (x1,y1), (x2,y2), color=(0,255,255), thickness=2)
        putText(frame, f'{x2-x1+1}x{y2-y1+1}', orig=(x1,y1-8))
        if not region.DOWN:  
            
            fgmask = bgsub.apply(trozo)
            cnts = cv.findContours(fgmask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]

            for cnt in cnts:
                    
                if cv.contourArea(cnt) > 500:
                    video.ON = True
                    masked = trozo.copy()
                    masked[fgmask==0] = 0
                    video.write(masked, video.ON)
                    cv.imshow('object', masked)
                    tiempo = time.time_ns()
            if ((time.time_ns()-tiempo)/ 1000000000) > 3:
                video.ON = False
    #video.write(trozo, video.ON)
    video.ON = False

   

    h,w,_ = frame.shape
    putText(frame, f'{w}x{h}')
    cv.imshow('input',frame)
cv.destroyAllWindows()
video.release()
