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

    (dX, dY) = (0, 0)
    direction = ""
    counti = 0
    # capture = cv2.VideoCapture('http://192.168.173.168:4745/mjpegfeed?1000x1080')
    capture = cv2.VideoCapture(1)
    # capture = cv2.VideoCapture('./vid2.mp4')
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
        for decoded in zbar_image:
            points = decoded.location
            print(decoded.data)
            if len(points) > 4:
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                hull = list(map(tuple, np.squeeze(hull)))
            else:
                hull = points;
            n = len(hull)
            for j in range(0, n):
                cv2.line(frame, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)

        frame = cv2.resize(frame, (800, 800))
        frame2 = frame
        blank_image = np.zeros((height, width, 3), np.uint8)
        blank_image = cv2.resize(blank_image, (800, 1000));
        arr = []
        lll = {}
        abra = False
        for decoded in zbar_image:
            abra = True
            lll[decoded.data] = True
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
                cv2.line(blank_image, (1500 - 500 - ll[0][0], ll[0][1]), (1500 - 500 - ll[2][0], ll[2][1]),
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
                             (100, (30 + hist[decoded.data][j][1] + hist[decoded.data][j][0]) % 254, 255), 10)
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
            # for j in arr:
            #     cv2.line(blank_image, (1500-500 - j[0], j[1]), (1500-500 - xa, ya), (0, 255, 255), 10)
            #     dist=math.sqrt((xa-j[0])**2+(ya-j[1])**2)
            #     if dist>0.1:
            #         cv2.putText(blank_image, "{0}".format(round(dist,2)), (1500-500-(xa+j[0])/2, (ya+j[1])/2+5 ), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0))

        count += 1

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
            print('hissss', hist[decoded.data][0])
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
                cv2.line(blank_image, (1500 - 500 - ll[0][0], ll[0][1]), (1500 - 500 - ll[2][0], ll[2][1]),
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
            # for j in arr:
            #     cv2.line(blank_image, (1500-500 - j[0], j[1]), (1500-500 - xa, ya), (0, 255, 255), 10)
            #     dist=math.sqrt((xa-j[0])**2+(ya-j[1])**2)
            #     if dist>0.1:
            #         cv2.putText(blank_image, "{0}".format(round(dist,2)), (1500-500-(xa+j[0])/2, (ya+j[1])/2+5 ), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0))

        if count > 4:
            q = []
            count = 0

        fframe = frame2
        fframe = fframe[1] if args.get("video", False) else fframe
        fframe = imutils.resize(fframe, width=600)
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

            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the fframe,
                # then update the list of tracked points
                cv2.circle(fframe, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
                cv2.circle(fframe, center, 5, (0, 0, 255), -1)
                pts.appendleft(center)

        # loop over the set of tracked points
        for i in np.arange(1, len(pts)):
            # if either of the tracked points are None, ignore
            # them
            if pts[i - 1] is None or pts[i] is None:
                continue

            # check to see if enough points have been accumulated in
            # the buffer
            if counter >= 10 and i == 1 and pts[-10] is not None:
                # compute the difference between the x and y
                # coordinates and re-initialize the direction
                # text variables
                dX = pts[-10][0] - pts[i][0]
                dY = pts[-10][1] - pts[i][1]
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
