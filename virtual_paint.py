import cv2
import numpy as np

#making our webcam to work:--
frame_width = 1000
frame_height = 1000
cap = cv2.VideoCapture(0)
cap.set(3,frame_width)
cap.set(4,frame_height)
cap.set(10,200)

myColors = [[67,143,37,86,255,255]]
myColorValues = [[178,255,102]]
myPoints = []


def findColors(img,myColors,myColorValues):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    
    for color in myColors:
        lower = np.asarray(color[0:3])
        upper = np.asarray(color[3:6])
        mask = cv2.inRange(img_hsv,lower,upper)
        x,y=getcontours(mask)
        cv2.circle(img_results,(x,y),(2),myColorValues[count],cv2.FILLED)
        newPoints.append([x,y,count])
        count +=1
        #cv2.imshow(str(color),mask)
    return newPoints
def getcontours(image):
    contours,hierarchy = cv2.findContours(image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        #print(area)
        if area>200:
            #cv2.drawContours(img_results,cnt,-1,(255,0,0),2)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x,y,w,h = cv2.boundingRect(approx)
    return x+w//2,y

def drawOnCanvas(myPoints,myColorValues):
    for points in myPoints:
        cv2.circle(img_results,(points[0],points[1]),(10),myColorValues[points[2]],cv2.FILLED)


while True:
    success, img = cap.read()
    img_results = img.copy()
    newPoints= findColors(img,myColors,myColorValues)
    for point in newPoints:
        myPoints.append(point)
    drawOnCanvas(myPoints,myColorValues)

        
    cv2.imshow("Video",img_results)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
