#!/usr/bin/env python

# eliminamos muchas coincidencias erróneas mediante el "ratio test"

import cv2 as cv
import time
import os


from umucv.stream import autoStream
from umucv.util import putText
from umucv.stream import Camera
from threading import Thread

imagenes = []
nomImagenes = []
rutaCarpetaImg = "imagenes/"

for img in os.listdir(rutaCarpetaImg):
    imagenes.append(cv.imread(rutaCarpetaImg + "/" + img))
    nomImagenes.append(img)


sift = cv.SIFT_create(nfeatures=500)

matcher = cv.BFMatcher()

x0 = None

def buscaMatches(keypoints,descriptors):

    global nombre
    global good
    
    indice = 0
    i = 0
    for img in imagenes:
        k0, d0 = sift.detectAndCompute(img, mask=None)
        goodAux = []
        matches = matcher.knnMatch(descriptors, d0, k=2)
        
        for m in matches:
            if len(m) >= 2:
                best,second = m
                if best.distance < 0.85*second.distance:
                    goodAux.append(best)

        if len(goodAux) > len(good):
            
            good = goodAux[0:len(goodAux)]
            indice = i

        i = i + 1

    nombre = nomImagenes[indice]


nombre = ""
good = []
for key,frame in autoStream():

    keypoints , descriptors = sift.detectAndCompute(frame, mask=None)
    flag = cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
    #cv.drawKeypoints(frame, keypoints, frame, color=(100,150,255), flags=flag)
    if key == ord('c'):
        
        good = []
        t = Thread(target=buscaMatches, args=(keypoints,descriptors))
        t.start()

    putText(frame ,f'{len(good)} matches')
    if len(good) > 20:
        putText(frame ,f'objeto: {nombre[0:len(nombre)-4]}',orig=(5,36), color=(200,255,200))  
    else:
        putText(frame ,f'objeto: {""}',orig=(5,36), color=(200,255,200))  
    cv.imshow("SIFT",frame)


