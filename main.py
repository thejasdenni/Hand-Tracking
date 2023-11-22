import cv2
from cvzone.HandTrackingModule import HandDetector
import socket

#Parameters
width, height = 640,480

#Webcam
cap = cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)


#Hand_Detection
detector=HandDetector(maxHands=1,detectionCon=0.8)

#Communication
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1",5052)


while True:
    #Get the frame from the webcam
    success, img = cap.read()
    #Hands
    hands, img =detector.findHands(img)

    data = []

    #Landmarks Values ~(x,y,z) * 21
    if hands:
        #Get the first hand detected
        hand =  hands[0]
        #Get the Landmark list
        lmList = hand['lmList']
        #print(lmList)
        for lm in lmList:
            data.extend([lm[0],height - lm[1],lm[2]])
        #print(data)
        sock.sendto(str.encode(str(data)),serverAddressPort)

    cv2.imshow("Image",img)
    cv2.waitKey(1)
