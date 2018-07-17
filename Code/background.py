import numpy as np
import cv2

def initialise():
	i=0
	print("Initialising")
	bg=np.zeros((height, width), np.uint8)	
	while(i<100):
		ret, img = cap.read()
		bg= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)	
		i+=1
	print("Done")	
    	return bg



upperbody_cascade = cv2.CascadeClassifier('haarcascade_mcs_upperbody.xml')
cap = cv2.VideoCapture(0)
ret, img = cap.read()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
height,width=gray.shape    
#sil= np.ones((height, width), np.uint8)*255
background= np.zeros((height, width), np.uint8)
background=initialise()

while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detected = upperbody_cascade.detectMultiScale(gray, 1.3, 5)
    sil=gray-background
    ret,sil = cv2.threshold(sil,127,255,cv2.THRESH_BINARY)
    sil = cv2.medianBlur(sil,5)		
    #if(len(detected)>0):
	#sil=np.ones((height, width), np.uint8)*255	
    #for (x,y,w,h) in detected:
        #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        #sil[y:, x:x+w] = gray[y:, x:x+w]
	#ret,sil = cv2.threshold(sil,127,255,cv2.THRESH_BINARY_INV)
    
    cv2.imshow('background',background)
    cv2.imshow('img',img)
    cv2.imshow('sil',sil)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
