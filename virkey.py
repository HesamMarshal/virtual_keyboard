# cv2  version 4.5.3
# cvzone version 1.4.1 TODO: Upgrade to latest version
# pynput v.1.7.3





import cv2  # version 4.5.3
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np

import cvzone
from pynput.keyboard import Controller            # pynput v.1.7.3


print('cv2.version:',cv2.__version__)
frame_width = 1280
frame_height = 720

DEFAULT_WEBCAM = 0
XPLIT_WEBCAM = 1
IRIUN_WEBCAM = 2


# TODO: Make COLOR Constants,
#  ALl Colors upercase ,
yellow = (0,255,255)
DARK_YELLOW = (0,175,175)
purple = (255,0,255)
white = (255,255,255)
GREEN = (0,255,0)
black = (0,0,0)
# TODO: Create more of them
key_color = yellow

cap = cv2.VideoCapture(IRIUN_WEBCAM)
#cap.set(3, frame_width)    # width
#cap.set(4, frame_height)     # height
print(F"Width =  {cap.get(3)}")
print(F"Height =  {cap.get(4)}")

dim = (frame_width, frame_height)

detecter = HandDetector(detectionCon=0.8)
keys = [["7","8","9"], ["4","5","6"],["1","2","3"]]
finalText = ""

keyboard = Controller()
def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                                   20, rt=0)
        cv2.rectangle(img, button.pos, (x + w, y + h), key_color, cv2.FILLED)
        cv2.putText(img, button.text, (x + 18, y + 70), cv2.FONT_HERSHEY_PLAIN, 4, black, 4)
    return img


# def drawAll(img, buttonList):
#     imgNew = np.zeros_like(img, np.uint8)
#     for button in buttonList:
#         x, y = button.pos
#         cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
#                           20, rt=0)
#         cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]),
#                       (255, 0, 255), cv2.FILLED)
#         cv2.putText(imgNew, button.text, (x + 40, y + 60),
#                     cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
#
#     out = img.copy()
#     alpha = 0.7
#     mask = imgNew.astype(bool)
#     #print(mask.shape)
#     out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
#     return out






class Button():
    def __init__(self,pos, text, size=[85,85]):
        self.pos = pos
        self.text = text
        self.size = size

    #def draw(self,img):

    #    return img

buttonList = []
base_loc = 300
for x in range(0, 3):
    buttonList.append(Button([base_loc + x * 90 + 50, 20], keys[0][x]))
    buttonList.append(Button([base_loc + x * 90 + 50, 110], keys[1][x]))
    buttonList.append(Button([base_loc + x * 90 + 50, 200], keys[2][x]))


while True:
    success, img = cap.read()
    # to detect the hand and fingers
    img = detecter.findHands(img)
    lmlist, bboxInfo = detecter.findPosition(img)
    img = drawAll(img,buttonList)

    if lmlist:
        for button in buttonList:
            x,y = button.pos
            w,h = button.size

            # TODO: Replace DARK_YELLOW with hover and set the hover to it.
            # TODO : Add select font at up.
            if x < lmlist[8][0] <x+w and y < lmlist[8][1]<y+h:
                cv2.rectangle(img, button.pos, (x + w, y + h), DARK_YELLOW, cv2.FILLED)
                cv2.putText(img, button.text, (x + 18, y + 70), cv2.FONT_HERSHEY_PLAIN, 4, black, 4)
                l,_,_ = detecter.findDistance(8,12,img,draw=False)


                # clicked
                if l < 20:
                    keyboard.press(button.text)
                    print(l)
                    cv2.rectangle(img, button.pos, (x + w, y + h),GREEN , cv2.FILLED)
                    cv2.putText(img, button.text, (x + 18, y + 70), cv2.FONT_HERSHEY_PLAIN, 4, black, 4)
                    finalText += button.text
                    sleep(0.5)

    cv2.rectangle(img, (50,350), (600,450), DARK_YELLOW, cv2.FILLED)
    cv2.putText(img, finalText, (60, 425), cv2.FONT_HERSHEY_PLAIN, 4, black, 4)





    #cv2.resize(img, dim, interpolation=cv2.INTER_AREA)  # (img, frameWidth, frameHeight)
    cv2.imshow("Image", img)
    cv2.waitKey(1)