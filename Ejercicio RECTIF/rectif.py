import numpy as np
import cv2   as cv

import matplotlib.pyplot as plt
from umucv.stream import autoStream
import math


def readrgb(file):
    return cv.cvtColor( cv.imread(file), cv.COLOR_BGR2RGB) 

def rgb2gray(x):
    return cv.cvtColor(x,cv.COLOR_RGB2GRAY)

def imshowg(x):
    plt.imshow(x, "gray")

black = True
img = readrgb('coins.png')
img[:, :, [0, 2]] = img[:, :, [2, 0]]

view = np.array([
        [325,460],
        [467,257],
        [625,312],
        [506,561]
        ])

real = np.array([
    [  50.,   280.],
    [ 260.,   280.],
    [ 260.,  380.],
    [  50.,  380.]])


H,_ = cv.findHomography(view, real)
rec = cv.warpPerspective(img,H,(800,600))
click1 = True
click2 = False
x1=0
y1=0
x2=0
y2=0
p1=()
p2=()

def manejador(event, x, y, flags, param):
    global click1
    global click2
    global x1
    global y1
    global x2
    global y2
    global band
    global p1
    global p2
    if event == cv.EVENT_LBUTTONDOWN:
        if click1:
            #print(str(x)+","+str(y))
            punto_original = np.array([[x, y]], dtype=np.float32)
            punto_original = np.reshape(punto_original, (1, 1, 2))
            punto_rectificada = cv.perspectiveTransform(punto_original, H)
            x1 = punto_rectificada[0][0][0]
            y1 = punto_rectificada[0][0][1]
            click1 = False
            click2 = True
            band = False
            p1=(x,y)
        elif click2:
            punto_original = np.array([[x, y]], dtype=np.float32)
            punto_original = np.reshape(punto_original, (1, 1, 2))
            punto_rectificada = cv.perspectiveTransform(punto_original, H)
            x2 = punto_rectificada[0][0][0]
            y2 = punto_rectificada[0][0][1]
            click2 = False
            click1 = True
            band = True
            p2=(x,y)

cv.namedWindow("imagen")
#cv.namedWindow("rec")
#cv.setMouseCallback("rec", manejador)
cv.setMouseCallback("imagen", manejador)
band = False
for key,frame in autoStream():

    if band:
        distancia = math.sqrt(((x2 - x1)*0.04)**2 + ((y2 - y1)*0.055)**2)
        texto_distancia = "Distancia: {:.2f}cm".format(distancia)
        cv.putText(img, texto_distancia, (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv.line(img,p1,p2,(255,0,0),2)
    else:
        img = img = readrgb('coins.png')
        img[:, :, [0, 2]] = img[:, :, [2, 0]]
    cv.imshow("imagen",img)
    #cv.imshow("rec",rec)