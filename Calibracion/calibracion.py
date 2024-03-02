#!/usr/bin/env python

import cv2 as cv
import numpy as np
from umucv.stream import autoStream

w= 960
h= 1280
f = 1125 # valor f en la matriz
click1 = 1
u = np.array(0)
v = np.array(0)
p1 = (0,0)
p2 = (0,0)

def manejador(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        print(x,y)
        global u
        global v
        global click1
        global p1
        global p2
        global imagen
        if click1 == 1:
            imagen = cv.imread(fn)
            cv.imshow('webcam',imagen)
            u = np.array([(x-w/2),(y-h/2),f])
            click1 = 2
            p1 = (x,y)
        elif click1 == 2:
            v = np.array([(x-w/2),(y-h/2),f]) 
            click1 = 3
            p2 = (x,y)
        if click1 == 3:
            proPunto = np.dot(u,v)
            magnitud = np.linalg.norm(u) * np.linalg.norm(v)
            angle = np.arccos(np.clip(proPunto/magnitud,-1,1))
            print(str(round(np.degrees(angle)))+ "º" )
            cv.line(imagen,p1,p2,(255,0,0),2)
            cv.imshow('webcam',imagen)
            click1 = 1


        

cv.namedWindow("webcam")
cv.setMouseCallback("webcam", manejador)
fn = "prueba.jpg"
imagen = cv.imread(fn)
cv.imshow('webcam',imagen)
cv.waitKey()
cv.destroyAllWindows()