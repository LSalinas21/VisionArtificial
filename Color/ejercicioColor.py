#!/usr/bin/env python

import cv2 as cv
from umucv.stream import autoStream
import numpy as np


def contarObjetos(contornos, color):
    cont = 1
    for (i,c) in  enumerate(contornos):
        area = cv.contourArea(c)
        if area > 2000:
            M = cv.moments(c)
            if (M["m00"]==0):
                M["m00"]=1
            x  = int(M["m10"]/M["m00"])
            y  = int(M["m01"]/M["m00"])
            cv.drawContours(imagen,[c], 0 , color, 2)
            cv.putText(imagen, str(cont), (x-10,y+10),1,2,(0,0,0),2)
            cont += 1

col = np.array([0,0,0], np.uint8)
azulBajo = np.array([80, 100, 20], np.uint8)
azulAlto = np.array([130, 255, 255], np.uint8)

naranjaBajo = np.array([10, 100, 20], np.uint8)
naranjaAlto = np.array([20, 255, 255], np.uint8)

violetaBajo = np.array([130, 100, 20], np.uint8)
violetaAlto = np.array([145, 255, 255], np.uint8)

verdeBajo = np.array([36, 100, 20], np.uint8)
verdeAlto = np.array([70, 255, 255], np.uint8)

amarilloBajo = np.array([21, 100, 20], np.uint8)
amarilloAlto = np.array([32, 255, 255], np.uint8)


rojoBajo1 = np.array([0, 100, 20], np.uint8)
rojoAlto1 = np.array([10, 255, 255], np.uint8)

rojoBajo2 = np.array([175, 100, 20], np.uint8)
rojoAlto2 = np.array([180, 255, 255], np.uint8)



def manejador(event, x, y, flags, param):
    global col

    if event == cv.EVENT_LBUTTONDOWN:
        col = np.array(imagenHSV[y][x], np.uint8)


cv.namedWindow("imagen")
cv.setMouseCallback("imagen", manejador)

imagen = cv.imread('colores1.png')
imagenCopia = imagen.copy()
imagenHSV = cv.cvtColor(imagen, cv.COLOR_BGR2HSV)

maskAmarillo = cv.inRange(imagenHSV, amarilloBajo, amarilloAlto)

maskAzul = cv.inRange(imagenHSV, azulBajo, azulAlto)
maskNaranja = cv.inRange(imagenHSV, naranjaBajo, naranjaAlto)
maskVerde = cv.inRange(imagenHSV, verdeBajo, verdeAlto)
maskVioleta = cv.inRange(imagenHSV, violetaBajo, violetaAlto)
maskRojo1 = cv.inRange(imagenHSV,rojoBajo1,rojoAlto1)
maskRojo2 = cv.inRange(imagenHSV,rojoAlto1,rojoAlto2)
maskRojo = cv.add(maskRojo1,maskRojo2)


contornosAmarillos, _ = cv.findContours(maskAmarillo,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
contornosAzul, _ = cv.findContours(maskAzul,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
contornosRojo, _ = cv.findContours(maskRojo,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
contornosVioleta, _ = cv.findContours(maskVioleta,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
contornosVerde, _ = cv.findContours(maskVerde,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
contornosNaranja, _ = cv.findContours(maskNaranja,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
key = 0
for key, frame in autoStream():
    cv.imshow("imagen", imagen)

    if not (col[1] == 0) and not (col[2] == 0) and not (col[0] == 255 and col[1] == 255 and col[3] == 255):
        if col[0] >= 21 and col[0]<=32:
            
            imagen = cv.imread('colores1.png')
            contarObjetos(contornosAmarillos,(0, 255, 255))
            col = np.array([0,0,0], np.uint8)
        elif col[0] >= 80 and col[0]<=130:
            
            imagen = cv.imread('colores1.png')
            contarObjetos(contornosAzul,(255, 0, 0))
            col = np.array([0,0,0], np.uint8)
        elif col[0] >= 36 and col[0]<=70:
            
            imagen = cv.imread('colores1.png')
            contarObjetos(contornosVerde,(0, 255, 0))
            col = np.array([0,0,0], np.uint8)
        elif ((col[0] >= 0 and col[0]<=10) or (col[0] >= 175 and col[0]<=180)):
            
            imagen = cv.imread('colores1.png')
            contarObjetos(contornosRojo,(0, 0, 255))
            col = np.array([0,0,0], np.uint8)
        elif col[0] >= 10 and col[0]<=20:
            
            imagen = cv.imread('colores1.png')
            contarObjetos(contornosNaranja,(0, 128, 255))
            col = np.array([0,0,0], np.uint8)
        elif col[0] >= 130 and col[0]<=145:
            
            imagen = cv.imread('colores1.png')
            contarObjetos(contornosVioleta,(200, 104, 186))
            col = np.array([0,0,0], np.uint8)
        if key == ord('q'):
            break   

cv.destroyAllWindows()
