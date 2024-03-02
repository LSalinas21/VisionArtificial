#!/usr/bin/env python
import cv2               as cv
from umucv.stream import autoStream
from scipy.ndimage import minimum_filter, maximum_filter
from umucv.util import ROI, putText

ayuda = cv.imread("ayuda.png")
def nada(x):
    pass

def creaMatriz(x):
    return (x,x)
def box(x):
    if x > 0:
        matriz = creaMatriz(x)
        copia = cv.boxFilter(trozo,-1,matriz)
        frame[y1+2:y2-1,x1+2:x2-1] = copia[0:len(copia)]

def gauss(x):
    if x > 0:
        auto = (0,0)
        copia = cv.GaussianBlur(trozo,auto,x)
        frame[y1+2:y2-1,x1+2:x2-1] = copia[0:len(copia)]
def maximo(x):
    if x > 0:
        copia = maximum_filter(trozo,x)
        frame[y1+2:y2-1,x1+2:x2-1] = copia[0:len(copia)]
def minimo(x):
    if x > 0:
        copia = minimum_filter(trozo,x)
        frame[y1+2:y2-1,x1+2:x2-1] = copia[0:len(copia)]

def median(x):
    if not (x %2) == 0:
        copia =cv.medianBlur(trozo,x)
        frame[y1+2:y2-1,x1+2:x2-1] = copia[0:len(copia)]

def bilateral(x):
    if x > 0:
        copia = cv.bilateralFilter(trozo,0,x,x)
        frame[y1+2:y2-1,x1+2:x2-1] = copia[0:len(copia)]

cv.namedWindow("input")
cv.createTrackbar("box","input", 1, 100,nada)
cv.createTrackbar("gauss","input", 1, 100,nada)
cv.createTrackbar("median","input", 1, 100,nada)
cv.createTrackbar("bilateral","input", 1, 100,nada)
cv.createTrackbar("minimun","input", 1, 100,nada)
cv.createTrackbar("maximun","input", 1, 100,nada)


opcion = 0
valorBox = cv.getTrackbarPos("box", "input")
valorGauss = cv.getTrackbarPos("gauss", "input")
valorMax = cv.getTrackbarPos("maximun", "input")
valorMin = cv.getTrackbarPos("minimun", "input")
valorMedian = cv.getTrackbarPos("median", "input")
valorBilateral = cv.getTrackbarPos("bilateral", "input")

mono = False
region = ROI("input")
trozo = []
for key, frame in autoStream():
    if mono:
        frame = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
    if region.roi:
        [x1,y1,x2,y2] = region.roi
        trozo = frame[y1+2:y2-1, x1+2:x2-1]
        cv.rectangle(frame, (x1,y1), (x2,y2), color=(0,255,255), thickness=2)
        putText(frame, f'{x2-x1+1}x{y2-y1+1}', orig=(x1,y1-8))

        if not region.DOWN:
            if key == ord("0"):
                opcion = 0
            elif key == ord("1"):
                opcion = key
            elif key == ord("2"):
                opcion = key
            elif key == ord("3"):
                opcion = key
            elif key == ord("4"):
                opcion = key
            elif key == ord("5"):
                opcion = key
            elif key == ord("6"):
                opcion = key

            if opcion == ord("1"):
                valorBox = cv.getTrackbarPos("box","input")
                box(valorBox)
            elif opcion == ord("2"):
                valorGauss = cv.getTrackbarPos("gauss","input")
                gauss(valorGauss)
            elif opcion == ord("3"):
                valorMedian = cv.getTrackbarPos("median","input")
                median(valorMedian)
            elif opcion == ord("4"):
                valorBilateral = cv.getTrackbarPos("bilateral","input")
                bilateral(valorBilateral)
            elif opcion == ord("6"):
                valorMax = cv.getTrackbarPos("maximun","input")
                maximo(valorMax)
            elif opcion == ord("5"):
                valorMin = cv.getTrackbarPos("minimun","input")
                minimo(valorMin)
        
    if key == ord("c"):
        if mono:
            mono = False
        else:
            mono = True

        
    cv.imshow("help", ayuda)
    cv.imshow('input', frame)
cv.destroyAllWindows()