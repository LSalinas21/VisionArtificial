import cv2          as cv
import numpy        as np
import math

from umucv.stream   import autoStream
from umucv.htrans   import htrans, Pose, homog
from umucv.util     import cube, showAxes
from umucv.contours import extractContours, redu


def Kfov(sz,hfovd):
    hfov = np.radians(hfovd)
    f = 1/np.tan(hfov/2)
    # print(f)
    w,h = sz
    w2 = w / 2
    h2 = h / 2
    return np.array([[f*w2, 0,    w2],
                     [0,    f*w2, h2],
                     [0,    0,    1 ]])


stream = autoStream()

HEIGHT, WIDTH = next(stream)[1].shape[:2]
size = WIDTH,HEIGHT


K = Kfov( size, 60 )


marker = np.array(
       [[0,   0,   0],
        [0,   1,   0],
        [0.5, 1,   0],
        [0.5, 0.5, 0],
        [1,   0.5, 0],
        [1,   0,   0]])

square = np.array(
       [[0,   0,   0],
        [0,   1,   0],
        [1,   1,   0],
        [1,   0,   0]])



def polygons(cs,n,prec=2):
    rs = [ redu(c,prec) for c in cs ]
    return [ r for r in rs if len(r) == n ]

def rots(c):
    return [np.roll(c,k,0) for k in range(len(c))]

def bestPose(K,view,model):
    poses = [ Pose(K, v.astype(float), model) for v in rots(view) ]
    return sorted(poses,key=lambda p: p.rms)[0]
    
def manejador(event, x, y, flags, param):
    global click
    global x1
    global y1
    x1=x
    y1=y
    click = True
x1=0
y1=0
click = False
objetivo=10
cv.namedWindow("source")
#cv.namedWindow("rec")
#cv.setMouseCallback("rec", manejador)
cv.setMouseCallback("source", manejador)
cosa = cube
xAnt=0
yAnt=0
sumX = False
sumY = False
for n, (key,frame) in enumerate(stream):

    g = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    cs = extractContours(g, minarea=5, reduprec=2)

    good = polygons(cs,6,3)
    
    poses = []
    for g in good:
        p = bestPose(K,g,marker)
        if p.rms < 2:
            poses += [p.M]
    poses = poses[:1]
    for M in poses:
        
        # capturamos el color de un punto cerca del marcador para borrarlo
        # dibujando un cuadrado encima
        if click:
            x,y = htrans(M, (0,0,0) ).astype(int)
            b,g,r = frame[y,x].astype(int)
        #cv.drawContours(frame,[htrans(M,square*1.1+(-0.05,-0.05,0)).astype(int)], -1, (int(b),int(g),int(r)) , -1, cv.LINE_AA)
        # cv.drawContours(frame,[htrans(M,marker).astype(int)], -1, (0,0,0) , 3, cv.LINE_AA)
        
        # Mostramos el sistema de referencia inducido por el marcador (es una utilidad de umucv)
            showAxes(frame, M, scale=0.5)
            x2,y2 = htrans(M, cosa[0] ).astype(int)

            # hacemos que se mueva el cubo
            distancia = math.sqrt(((x2 - x1))**2 + ((y2 - y1))**2)
            punto = np.array([x2,y2,0])
            punto_pixeles = np.array([x1, y1, 1])
            punto_3D_homogeneo = np.linalg.pinv(M) @ punto_pixeles
            punto_3D = punto_3D_homogeneo[:3] / punto_3D_homogeneo[3]
            
            if distancia > 1:
                if punto_3D[0] > cosa[0][0]:
                    sumX = True
                    xAnt+=0.03
                else:
                    sumX = True
                    xAnt-=0.03            
                if punto_3D[1] > cosa[0][1]:
                    sumY = True
                    yAnt+=0.03
                else:
                    sumY = True
                    yAnt-=0.03

            if sumX and sumY:
                cosa = cube * (0.5,0.5,0.5) + (xAnt,yAnt,0)
            elif sumX:
                cosa = cube * (0.5,0.5,0.5) + (xAnt,0,0)
            elif sumY:
                cosa = cube * (0.5,0.5,0.5) + (0,yAnt,0)
            sumX = False
            sumY = False
            cv.drawContours(frame, [ htrans(M, cosa).astype(int) ], -1, (0,128,0), 3, cv.LINE_AA)

    cv.imshow('source',frame)