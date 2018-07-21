import zbar
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from PIL import Image
#import pyzbar.pyzbar as pyzbar
import numpy as np
import  urllib
import imutils
from math import atan2
import math
import random
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import cv2.aruco as aruco
import glob
import imutils
import time
import numpy as np
import cv2


def main():
    """
    aaaa
    """
    # default cam matrix rows and columns
    cap = cv2.VideoCapture(0)  # use external cam
    upperbody_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # get the background and resize it.
    img_back = cv2.imread('black.jpg')
    background_color = np.uint8([[[0, 0, 255]]])
    hls_background_color = cv2.cvtColor(background_color, cv2.COLOR_BGR2HLS)
    hls_background_color = hls_background_color[0][0]
    while True:


        ret, frame = cap.read()
        image = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        detected = upperbody_cascade.detectMultiScale(image, 1.3, 5) 
      	silhoutte=np.zeros(image.shape,np.uint8)
	image = cv2.blur(image,(15,15))
        (_,img_th) = cv2.threshold(image,96,255,1)
        _, contours, _ = cv2.findContours(img_th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(silhoutte,contours,-1,(255,0,0),2)	
	for (x,y,w,h) in detected:
             cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
             #silhoutte[y:, x-w:x+(2*w)] = image[y:, x-w:x+(2*w)]
	     silhoutte[y:, x+(2*w)-1:] = 0
	     silhoutte[y:, :x-w+1] = 0		
        _, contours, _ = cv2.findContours(silhoutte, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)	
	maximum=0
	point=[]
	max_area=[]
	for c in contours:
		if(cv2.contourArea(c)>maximum):
			maximum=cv2.contourArea(c)
			max_area=c

	#contour_length.sort(reverse=True)
	#contour_length=contour_length[:len(contour_length)/2]
	#print(contour_length)	
	#for c in contours:		
		#if len(c) in contour_length and cv2.contourArea(c) > 300: 
				#point.append(c)
	#print("len",len(point))
	#print(point)
	h,w=image.shape
        silhoutte=np.zeros((h,w,3),np.uint8)
	sil_arr = np.vstack(max_area).squeeze()        
	#print(len(sil_arr[:5]))	
	#cv2.drawContours(silhoutte,contours,-1,(255,0,0),2)	
	#cv2.drawContours(silhoutte,point,-1,(255,0,0),2)
	   	
	#print (max_area)
	cv2.drawContours(silhoutte,max_area,-1,(255,0,0),2)
	cv2.fillConvexPoly(silhoutte, sil_arr, (0,255,0), lineType=8, shift=0)        
	cv2.imshow("hi.jpg",image)
	cv2.imshow("Silhoutte",silhoutte)
        # cols, rows = frame.shape[:2]
        
        # background = img_back[0:cols, 0:rows]
        # frame = cv2.flip(frame, 1, frame)

        # hls_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)

        # hue = hls_image[:, :, 0]

        # binary_hue = cv2.inRange(hue, 100, 120)

        # mask = np.zeros(hls_image.shape, dtype=np.uint8)

        # mask[:, :, 0] = binary_hue
        # mask[:, :, 1] = binary_hue
        # mask[:, :, 2] = binary_hue

        # blured = cv2.GaussianBlur(mask, (11, 11), 0)
        # blured_inverted = cv2.bitwise_not(blured)
        # bg_key = cv2.bitwise_and(background, blured)
        # fg_key = cv2.bitwise_and(frame, blured_inverted)
        # cv2.imwrite('bg.jpg', bg_key)
        # cv2.imwrite('fg.jpg', fg_key)
        # keyed = cv2.add(bg_key, fg_key)
        
        # gray = cv2.cvtColor(keyed, cv2.COLOR_BGR2GRAY)

        # detected = upperbody_cascade.detectMultiScale(gray, 1.3, 5)
        # h,w=gray.shape
        # blank1=np.zeros((h,w,3),np.uint8)
        # blank=np.zeros(gray.shape,np.uint8)
        # for (x,y,w,h) in detected:
        #     cv2.rectangle(keyed,(x,y),(x+w,y+h),(255,0,0),2)
        #     blank[y:, x-w:x+(2*w)] = gray[y:, x-w:x+(2*w)]
        # edges=cv2.Canny(blank,100,200)
        # _,thresh=cv2.threshold(blank,96,255,1)    
        # _,contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 
        # p=[]
        # for c in contours:
        #     if cv2.contourArea(c)>15:
        #         x,y,w,h=cv2.boundingRect(c)
        #         p.append(c)
        # # if len(contours) > 4:
        # #         hull = cv2.convexHull(np.array([point[0] for point in contours], dtype=np.int32))
        # #         hull = list(map(tuple, np.squeeze(hull)))
        # # else:

        # #     hull = contours;
        # # n = len(hull)
        # # #print(hull)
            
        # # for j in range(0, n):
        # #     cv2.line(blank1, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)
        # print("No. Of contours",len(p))
        # # print contours
        
        # cv2.drawContours(blank1, p, -1, (255,0,0), 3)
        # cv2.imshow("Thresh",thresh)
        # cv2.imshow('frame', keyed)
        # cv2.imshow('contour',blank1)
        # cv2.imshow("edges",edges)
        k = cv2.waitKey(33)
        if k == 27:  # ESC
            break

if __name__ == "__main__":
    main()
