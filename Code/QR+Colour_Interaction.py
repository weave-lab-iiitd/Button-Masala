import zbar
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from PIL import Image
import pyzbar.pyzbar as pyzbar
import numpy as np
import  urllib
import imutils
import math
import random
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32,
	help="max buffer size")
args = vars(ap.parse_args())
# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
counter = 0
pts = deque(maxlen=args["buffer"])

(dX, dY) = (0, 0)
direction = ""



def find_centre(points):
	meanx=0
	meany=0
	for point in points:
		x,y=point
		meanx+=x
		meany+=y
	return (meanx,meany)

def Zoom(objj, size):
    objj = imutils.resize(objj, width=(size * objj.shape[1]))
    point = (objj.shape[0] / 2, objj.shape[1] / 2)
    scll = (point[0] / size, point[1] / size)
    objj = objj[scll[0]:(point[0] + scll[0]), scll[1]:(point[1] + scll[1])]
    return objj


def main():
    hist = {}
    q = []
    counter = 0
    pts = deque(maxlen=args["buffer"])

    #variables for QR_code Connection

    centres=[]
    qr_conn=[]
    qr_conn1=[]
    ccc=None
    (dX, dY) = (0, 0)
    direction = ""
    conn=[]
    counti = 0
    capture = cv2.VideoCapture('http://192.168.173.168:4745/mjpegfeed?1000x1080')
    #capture = cv2.VideoCapture(1)
    #capture = cv2.VideoCapture('vid2.mp4')
    count = 0
    vs=capture
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        ret, frame = capture.read()


        resize = cv2.resize(frame, (700, 800));
        # cv2.imshow('Current',resize)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        image = Image.fromarray(gray)
        width, height = image.size
        zbar_image = zbar.Image(width, height, 'Y800', image.tobytes())
        scanner = zbar.ImageScanner()
        scanner.scan(zbar_image)
        if len(hist)<len(qr_conn):qr_conn = qr_conn[len(qr_conn)-1-(len(qr_conn)-len(hist)):len(qr_conn)-1]
        if len(conn)<1:
            cv2.line(frame,(0,0),(0,0) , (30, 90, 235), 1)
        for l in range(len(conn)-1):
            #print('lol  ',tuple(hist[conn[l].data][-1]),tuple(hist[conn[l+1].data][-1]))
            cv2.line(frame, tuple(hist[conn[l].data][-1]),tuple(hist[conn[l+1].data][-1]) , (30, 90, 235), 5)
            #cv2.line(frame, tuple(hist[conn[l].data][-1]),tuple(hist[conn[l+1].data][-1]) , (255, 255, 255), 5)

            #if l==len(conn)-1:
                #cv2.line(frame, tuple(hist[conn[l+1].data][-1]), tuple(hist[conn[0].data][-1]), (30, 90, 235), 5)

        for decoded in zbar_image:
            points = decoded.location
            #print(decoded.data)
            if len(points) > 4:
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                hull = list(map(tuple, np.squeeze(hull)))
            else:
                hull = points;
            n = len(hull)
            #print(hull)
            try:
                c1 = hull[0][0] + hull[1][0] + hull[2][0] + hull[3][0]
                c2 = hull[0][1] + hull[1][1] + hull[2][1] + hull[3][1]
                c1 /= 4;
                c2 /= 4
            except:
                continue
            for j in range(0, n):
                cv2.line(frame, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)

            cv2.line(frame, (c1,c2), (c1,c2), (255, 255, 0), 3)
            # if (math.sqrt((xa - xb) ** 2 + (ya - yb) ** 2) < threshold):
            #     cv2.circle(blank_image, (xa, ya), 20, (0, 255, 0), -1)
            #     if (xa, ya) not in qr_conn:
            #         qr_conn.append((xa, ya))
            #
            # if (len(qr_conn) > 0):
            #     cv2.line(blank_image, qr_conn[len(qr_conn) - 1], (xb, yb), (0, 255, 255), 5)
            #     for i in range(0, len(qr_conn) - 1):
            #         cv2.line(blank_image, qr_conn[i], qr_conn[i + 1], (0, 255, 255), 5)
#Code For Connecting  QR_Codes.
        #print ("center:",centres)
	#needs code for setting an adaptive threshold

            threshold=110 #set an appropriate threshold for distance between finger and QRcentre
            if(ccc != None):
                center=ccc
                #print('yas')
                #For connection in Blank image
                xa,ya=c1,c2
                ya=ya
                xb,yb=center
                xb=abs(980-xb-40)
                yb=(yb)
                cv2.circle(frame,(c1,c2), 5, (255, 0, 255), -1)
                #cv2.circle(frame,(xa,ya),10,(0, 255,0 ), -1)

                print('c2,c2',c1," ",c2,"xb,yb",xb," ",yb)
                print("distance:",math.sqrt((xa-xb)**2+(ya-yb)**2))
                if(math.sqrt((xa-xb)**2+(ya-yb)**2)<threshold):
                    cv2.circle(frame,(c1,c2),20,(255, 0,255 ), -1)

                    conn.append(decoded)
                    if (xa,ya) not in qr_conn:
                        qr_conn.append((xa,ya))
                print(qr_conn)
                # if(len(qr_conn)>0):
                #      cv2.line(frame, qr_conn[len(qr_conn)-1], (xb,yb) , (30, 90, 235), 5)
                #      for i in range(0,len(qr_conn)-1):
                #          cv2.line(frame, qr_conn[i], qr_conn[i+1] , (30, 90, 235), 5)

                # #For connection in Real Time Video
                # for point in arr:
                #     xa,ya=point
                #     xa=xa
                #     ya=ya
                #     xb,yb=center
                #
                #     cv2.circle(fframe,(c1,c2),10,(0, 255,0 ), -1)
                #     #print("distance:",math.sqrt((xa-xb)**2+(ya-yb)**2))
                #     if(math.sqrt((xa-xb)**2+(ya-yb)**2)<threshold):
                #         cv2.circle(fframe,(xa,ya),20,(0, 255,0 ), -1)
                #         if (xa,ya) not in qr_conn1:
                #             qr_conn1.append((xa,ya))
                #
                #
                #
                # if(len(qr_conn1)>0):
                #     cv2.line(fframe, qr_conn1[len(qr_conn1)-1], center , (0, 255, 255), 5)
                #     for i in range(0,len(qr_conn1)-1):
                #         cv2.line(fframe, qr_conn1[i], qr_conn1[i+1] , (0, 255, 255), 5)



        frame = cv2.resize(frame, (800, 800))
        frame2 = frame
        blank_image = np.zeros((height, width, 3), np.uint8)
        blank_image = cv2.resize(blank_image, (800, 1000));
        arr = []
        lll = {}
        abra = False
        centresl=[]
        for decoded in zbar_image:
            abra = True
            lll[decoded.data] = True
            points = decoded.location

	    #centresl.append(find_centre(points))

            ll = [point for point in points]
            # x1=min(1500-500-ll[0][0],ll[1][0],ll[2][0],ll[3][0])#top-left pt. is the leftmost of the 4 points
            # x2=max(1500-500-ll[0][0],ll[1][0],ll[2][0],ll[3][0])#bottom-right pt. is the rightmost of the 4 points
            # y1=min(1500-500-ll[0][1],ll[1][1],ll[2][1],ll[3][1])#top-left pt. is the uppermost of the 4 points
            # y2=max(1500-500-ll[0][1],ll[1][1],ll[2][1],ll[3][1])#bottom-right pt. is the lowermost of the 4 points
            # print("coordinates")
            # cv2.line(blank_image,(h1,h2),(1500-500-ll[0][0],ll[0][1]),(255,255,255),15)
            try:
                cv2.line(blank_image, (1500 - 500 - ll[0][0], ll[0][1]), (1500 - 500 - ll[1][0], ll[1][1]),
                         (255, 255, 255), 10)
                cv2.line(blank_image, (1500 - 500 - ll[1][0], ll[1][1]), (1500 - 500 - ll[2][0], ll[2][1]),
                         (255, 255, 255), 10)
                cv2.line(blank_image, (1500 - 500 - ll[2][0], ll[2][1]), (1500 - 500 - ll[3][0], ll[3][1]),
                         (255, 255, 255), 10)
                cv2.line(blank_image, (1500 - 500 - ll[3][0], ll[3][1]), (1500 - 500 - ll[0][0], ll[0][1]),
                         (255, 255, 255), 10)

                cv2.line(blank_image, (1500 - 500 - ll[2][0], ll[2][1]), (1500 - 500 - ll[2][0], ll[2][1]), (0, 0, 255),
                         25)
            except:
                continue
            xa = ll[0][0] + ll[1][0] + ll[2][0] + ll[3][0]
            ya = ll[0][1] + ll[1][1] + ll[2][1] + ll[3][1]
            xa /= 4;
            ya /= 4
            lx, ly = xa, ya
            lol = 1
            try:
                # print(hist[decoded.data])
                for j in range(2, len(hist[decoded.data])):
                    lol += 1
                    if lol <= 2:
                        lx = hist[decoded.data][j][0]
                        ly = hist[decoded.data][j][1]
                        continue
                    # print('lowllal',decoded.data,j[0])
                    # print "yaaaa",hist[decoded.data][j],hist[decoded.data][j+1],

                    cv2.line(blank_image, (1500 - 500 - lx, ly),
                             (1500 - 500 - hist[decoded.data][j][0], hist[decoded.data][j][1]),
                             (100, (30 + hist[decoded.data][j][1] + hist[decoded.data][j][0]) % 254, 255), 5)
                    lx = hist[decoded.data][j][0]
                    ly = hist[decoded.data][j][1]
                    # print 'lo', lx, ly
            except:
                # print 'la',lx, ly
                cv2.line(blank_image, (1500 - 500 - lx, ly),
                         (1500 - 500 - lx, ly), (100, 30, 255), 10)
            arr.append((xa, ya))
            try:
                hist[decoded.data].append([xa, ya])
                hist[decoded.data][0] = 0
                hist[decoded.data][1] = decoded
            except:
                hist[decoded.data] = [0, decoded, [xa, ya]]
            # print('lenggg',len(hist))
            if len(hist[decoded.data]) > 80:
                del hist[decoded.data][2]
            for j in arr:
                cv2.line(blank_image, (1500-500 - j[0], j[1]), (1500-500 - xa, ya), (0, 255, 255), 5)
                dist=math.sqrt((xa-j[0])**2+(ya-j[1])**2)
                if dist>0.1:
                    cv2.putText(blank_image, "{0}".format(round(dist,2)), (1500-500-(xa+j[0])/2, (ya+j[1])/2+5 ), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0))

	#print("Centres:",centres)
        count += 1
#	if(len(arr)>=len(centres)):
		#centres=arr

	for j in hist:
            if hist[j][0] > 0:
                q.append(hist[j][1])

        for j in hist:
            try:
                hist[j][0] += 1
            except:
                hist[j][0] = 1

        for decoded in q:
            if abra == False:

                continue
            #print('hissss', hist[decoded.data][0])
            if hist[decoded.data][0] > 20:
                continue
            try:
                if lll[decoded.data]:
                    continue
            except:
                pass
            points = decoded.location
            ll = [point for point in points]
            # x1=min(1500-500-ll[0][0],ll[1][0],ll[2][0],ll[3][0])#top-left pt. is the leftmost of the 4 points
            # x2=max(1500-500-ll[0][0],ll[1][0],ll[2][0],ll[3][0])#bottom-right pt. is the rightmost of the 4 points
            # y1=min(1500-500-ll[0][1],ll[1][1],ll[2][1],ll[3][1])#top-left pt. is the uppermost of the 4 points
            # y2=max(1500-500-ll[0][1],ll[1][1],ll[2][1],ll[3][1])#bottom-right pt. is the lowermost of the 4 points
            # print("coordinates")
            # cv2.line(blank_image,(h1,h2),(1500-500-ll[0][0],ll[0][1]),(255,255,255),15)
            try:
                cv2.line(blank_image, (1500 - 500 - ll[0][0], ll[0][1]), (1500 - 500 - ll[1][0], ll[1][1]),
                         (255, 255, 255), 10)
                cv2.line(blank_image, (1500 - 500 - ll[1][0], ll[1][1]), (1500 - 500 - ll[2][0], ll[2][1]),
                         (255, 255, 255), 10)
                cv2.line(blank_image, (1500 - 500 - ll[2][0], ll[2][1]), (1500 - 500 - ll[3][0], ll[3][1]),
                         (255, 255, 255), 10)
                cv2.line(blank_image, (1500 - 500 - ll[3][0], ll[3][1]), (1500 - 500 - ll[0][0], ll[0][1]),
                         (255, 255, 255), 10)

                cv2.line(blank_image, (1500 - 500 - ll[2][0], ll[2][1]), (1500 - 500 - ll[2][0], ll[2][1]), (0, 0, 255),
                         25)
            except:
                continue
            xa = ll[0][0] + ll[1][0] + ll[2][0] + ll[3][0]
            ya = ll[0][1] + ll[1][1] + ll[2][1] + ll[3][1]
            xa /= 4;
            ya /= 4
            # font = cv2.FONT_HERSHEY_SIMPLEX
            # cv2.putText(blank_image, decoded.data, (xa, ya), font, 2, (255, 255, 255), 2, cv2.LINE_AA)
            lx, ly = xa, ya
            lol = 1
            try:
                # print(hist[decoded.data])
                for j in range(2, len(hist[decoded.data])):
                    lol += 1
                    if lol <= 2:
                        lx = hist[decoded.data][j][0]
                        ly = hist[decoded.data][j][1]
                        continue
                    # print('lowllal',decoded.data,j[0])
                    # print "yaaaa",hist[decoded.data][j],hist[decoded.data][j+1],
                    cv2.line(blank_image, (1500 - 500 - lx, ly),
                             (1500 - 500 - hist[decoded.data][j][0], hist[decoded.data][j][1]),
                             (100, (30 + hist[decoded.data][j][1] + hist[decoded.data][j][0]) % 254, 255), 7)
                    lx = hist[decoded.data][j][0]
                    ly = hist[decoded.data][j][1]
                    # print 'lo', lx, ly
            except:
                # print 'la',lx, ly
                cv2.line(blank_image, (1500 - 500 - lx, ly),
                         (1500 - 500 - lx, ly), (100, 30, 255), 10)
            arr.append((xa, ya))
            try:
                hist[decoded.data].append([xa, ya])
                hist[decoded.data][0] += 1
                hist[decoded.data][1] = decoded
            except:
                hist[decoded.data] = [1, decoded, [xa, ya]]
            # print('lenggg',len(hist))
            if len(hist[decoded.data]) > 100:
                del hist[decoded.data][2]
            for j in arr:
                cv2.line(blank_image, (1500-500 - j[0], j[1]), (1500-500 - xa, ya), (0, 255, 255), 5)
                dist=math.sqrt((xa-j[0])**2+(ya-j[1])**2)
                if dist>0.1:
                    cv2.putText(blank_image, "{0}".format(round(dist,2)), (1500-500-(xa+j[0])/2, (ya+j[1])/2+5 ), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0))

        if count > 4:
            q = []
            count = 0

        fframe = frame2
        fframe = fframe[1] if args.get("video", False) else fframe
        fframe = imutils.resize(fframe, width=800,height=1000)
        blurred = cv2.GaussianBlur(fframe, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV);
        hsv = cv2.flip(hsv, 1);
        fframe = cv2.flip(fframe, 1)
        mask = cv2.inRange(hsv, greenLower, greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            ccc=center
            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the fframe,
                # then update the list of tracked points
                cv2.circle(fframe, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
                cv2.circle(fframe, center, 5, (0, 0, 255), -1)
		pts.appendleft(center)

	#lololol


        # loop over the set of tracked points
        for i in np.arange(1, len(pts)):
            # if either of the tracked points are None, ignore
            # them
            if pts[i - 1] is None or pts[i] is None:
                continue

            # check to see if enough points have been accumulated in
            # the buffer
            if counter >= 10 and i == 1 and pts[-1] is not None:
                # compute the difference between the x and y
                # coordinates and re-initialize the direction
                # text variables
                dX = pts[-1][0] - pts[i][0]
                dY = pts[-1][1] - pts[i][1]
                (dirX, dirY) = ("", "")

                # ensure there is significant movement in the
                # x-direction
                if np.abs(dX) > 20:
                    dirX = "East" if np.sign(dX) == 1 else "West"

                # ensure there is significant movement in the
                # y-direction
                if np.abs(dY) > 20:
                    dirY = "North" if np.sign(dY) == 1 else "South"

                # handle when both directions are non-empty
                if dirX != "" and dirY != "":
                    direction = "{}-{}".format(dirY, dirX)

                # otherwise, only one direction is non-empty
                else:
                    direction = dirX if dirX != "" else dirY

            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
            cv2.line(fframe, pts[i - 1], pts[i], (0, 0, 255), thickness)
            # show the movement deltas and the direction of movement on
            # the fframe
        cv2.putText(fframe, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (0, 0, 255), 3)
        cv2.putText(fframe, "dx: {}, dy: {}".format(dX, dY),
                    (10, fframe.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.35, (0, 0, 255), 1)

        # show the fframe to our screen and increment the fframe counter
        counter += 1
        cv2.imshow("input", fframe)

        cv2.imshow("Output", blank_image)


if __name__ == "__main__":
    main()
