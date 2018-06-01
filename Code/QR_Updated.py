import zbar
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from PIL import Image
import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2,urllib
import imutils
import math
def Zoom(objj, size):
    objj = imutils.resize(objj, width=(size * objj.shape[1]))
    point = (objj.shape[0]/2,objj.shape[1]/2)
    scll = (point[0]/size, point[1]/size)
    objj = objj[scll[0]:(point[0] + scll[0]), scll[1]:(point[1] + scll[1])]
    return objj
def main():
    capture = cv2.VideoCapture(0)

    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        ret, frame = capture.read()
        #frame = Zoom(frame, 1)

        resize = cv2.resize(frame, (700, 800));

        #cv2.imshow('Current',resize)

        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        image = Image.fromarray(gray)
        width, height = image.size
        zbar_image = zbar.Image(width, height, 'Y800', image.tobytes())
        scanner = zbar.ImageScanner()
        scanner.scan(zbar_image)

        for decoded in zbar_image:
            points=decoded.location
            print(decoded.data)
            if len(points) > 4:
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                hull = list(map(tuple, np.squeeze(hull)))
            else:
                hull = points;
            n = len(hull)
            for j in range(0, n):
                cv2.line(frame, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)
        frame = cv2.resize(frame, (800, 800));
        blank_image = np.zeros((height, width, 3), np.uint8)
        blank_image = cv2.resize(blank_image, (1500-200-500, 1000));
        cv2.imshow("Results", frame);
        arr=[]
        for decoded in zbar_image:
            points=decoded.location
            ll=[point for point in points]
            # x1=min(1500-200-500-ll[0][0],ll[1][0],ll[2][0],ll[3][0])#top-left pt. is the leftmost of the 4 points
            # x2=max(1500-200-500-ll[0][0],ll[1][0],ll[2][0],ll[3][0])#bottom-right pt. is the rightmost of the 4 points
            # y1=min(1500-200-500-ll[0][1],ll[1][1],ll[2][1],ll[3][1])#top-left pt. is the uppermost of the 4 points
            # y2=max(1500-200-500-ll[0][1],ll[1][1],ll[2][1],ll[3][1])#bottom-right pt. is the lowermost of the 4 points
            #print("coordinates")
            #cv2.line(blank_image,(h1,h2),(1500-200-500-ll[0][0],ll[0][1]),(255,255,255),15)

            cv2.line(blank_image,(1500-200-500-ll[0][0],ll[0][1]),(1500-200-500-ll[1][0],ll[1][1]),(255,255,255),25)
            cv2.line(blank_image,(1500-200-500-ll[1][0],ll[1][1]),(1500-200-500-ll[2][0],ll[2][1]),(255,255,255),25)
            cv2.line(blank_image,(1500-200-500-ll[2][0],ll[2][1]),(1500-200-500-ll[3][0],ll[3][1]),(255,255,255),25)
            cv2.line(blank_image,(1500-200-500-ll[3][0],ll[3][1]),(1500-200-500-ll[0][0],ll[0][1]),(255,255,255),25)
            cv2.line(blank_image,(1500-200-500-ll[0][0],ll[0][1]),(1500-200-500-ll[2][0],ll[2][1]),(255,255,255),25)
            cv2.line(blank_image,(1500-200-500-ll[2][0],ll[2][1]),(1500-200-500-ll[2][0],ll[2][1]),(0,0,255),25)
            xa=ll[0][0]+ll[1][0]+ll[2][0]+ll[3][0]
            ya=ll[0][1]+ll[1][1]+ll[2][1]+ll[3][1]
            xa/=4;ya/=4
            arr.append((xa,ya))
            for j in arr:
                cv2.line(blank_image, (1500-200-500 - j[0], j[1]), (1500-200-500 - xa, ya), (0, 255, 255), 25)
                dist=math.sqrt((xa-j[0])**2+(ya-j[1])**2)
                if dist>0.1:
                    cv2.putText(blank_image, "{0}".format(dist), (1500-200-500-(xa+j[0])/2, (ya+j[1])/2+5 ), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))

        cv2.imshow("lol", blank_image);


if __name__ == "__main__":
    main()