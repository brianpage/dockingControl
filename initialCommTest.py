import socket
import cv2
import numpy as np
from NMEA import NMEAparse
# import matplotlib.pyplot as plt

TCP_IP = '192.168.1.26'
TCP_PORT = 29500
BUFFER_SIZE = 1024
MESSAGE = "$BPLOG,ALL,ON\r\n"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
parser=NMEAparse()

data = s.recv(BUFFER_SIZE)
data=data.decode()

# print("startup",data.decode())
s.sendall(MESSAGE.encode('ascii'))
# s.shutdown(socket.SHUT_WR)

count=0
while count < 5:
        data = s.recv(BUFFER_SIZE)
        data=data.decode()
        print(data)
        parsed=parser.parse(data)
        print(parsed.messageType)


        # print("loop",data.decode('ascii'))
        count=count+1
        print(count)
s.close()


# #img=cv2.imread('image.jpg',cv2.IMREAD_GRAYSCALE)

# #cv2.imshow('image',img)
# #cv2.waitKey(0)
# #cv2.destroyAllWindows()

# cap=cv2.VideoCapture(0)

# #fourcc=cv2.VideoWriter_fourcc(*'XVID')
# #out=cv2.VideoWriter('output.avi',fourcc,20.0,(640,480))

# params=cv2.SimpleBlobDetector_Params()
# params.minThreshold=200
# params.maxThreshold=255

# params.filterByColor=True
# params.blobColor=255

# params.filterByArea=True
# params.minArea=100

# params.filterByCircularity=True
# params.minCircularity=0.7

# params.filterByConvexity=False
# params.minConvexity=0.8

# params.filterByInertia=False
# params.minInertiaRatio=0.8
# detector=cv2.SimpleBlobDetector_create(params)

# while True:
#         _, frame=cap.read()
#         gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
#         #hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
#         #retval,threshold=cv2.threshold(gray,235,255,cv2.THRESH_BINARY)
#         #threshold=cv2.bilateralFilter(threshold,15,75,75)
#         #threshold=cv2.medianBlur(threshold,3)
#         #gauss=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,115,1)
#         #retval,otsu=cv2.threshold(gray,125,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#         keypoints=detector.detect(gray)
#         if keypoints!=[]:
#                 for keypoint in keypoints:
#                         x=keypoint.pt[0]
#                         y=keypoint.pt[1]
#                         size=keypoint.size
#         else:
#                 x=-1
#                 size=-1
#                 y=-1
#         print(x,y,size)

