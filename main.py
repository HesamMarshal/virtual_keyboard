# cv2  version 4.5.3
# mediapipe version 0.8.7
# cvzone version 1.5.3
# pynput v.1.7.3

import cv2  # version 4.5.3
from cvzone.HandTrackingModule import HandDetector
import cvzone
from pynput.keyboard import Controller
import constant

print('cv2.version:', cv2.__version__)

# CONFIG
FONT_FAMILY = cv2.FONT_HERSHEY_PLAIN

FONT_COLOR = constant.BLACK
KEY_COLOR = constant.YELLOW
HOVER = constant.DARK_YELLOW
KEY_DIVIDER = constant.GREEN

CLICK_SIZE = constant.CLICK_SIZE

cap = cv2.VideoCapture(constant.WEBCAM, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, constant.FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, constant.FRAME_HEIGHT)

detector = HandDetector(detectionCon=0.8)
keys = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"]]
finalText = ""

keyboard = Controller()


class Button():
    def __init__(self, pos, text, size=[85, 85], is_alpha_num=True):
        self.pos = pos
        self.is_alpha_num = is_alpha_num
        self.text = text
        self.size = size

    # def draw(self,img):
    #    return img


# Position of numbers on the image
buttonList = []
base_x_loc = 800
base_y_loc = 250
for x in range(0, 3):
    buttonList.append(Button([base_x_loc + x * 90 + 50, base_y_loc], keys[0][x]))
    buttonList.append(Button([base_x_loc + x * 90 + 50, base_y_loc + 90], keys[1][x]))
    buttonList.append(Button([base_x_loc + x * 90 + 50, base_y_loc + 180], keys[2][x]))

buttonList.append(Button([100, 200], 'Exit', size=[160, 85], is_alpha_num=False))
buttonList.append(Button([100, 300], 'Clear', size=[200, 85], is_alpha_num=False))
# buttonList.append(Button([100, 400], 'Del', size=[200, 85], is_alpha_num=False))



def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(
            img, (button.pos[0], button.pos[1], button.size[0], button.size[1]), 20, rt=0)
        cv2.rectangle(img, button.pos, (x + w, y + h), KEY_COLOR, cv2.FILLED)
        cv2.putText(img, button.text, (x + 18, y + 70),
                    cv2.FONT_HERSHEY_PLAIN, 4, FONT_COLOR, 4)
    return img

exit_pressed = False
click_released = True
print('CLICK_SIZE : ', CLICK_SIZE)
while not exit_pressed:
    success, img = cap.read()

    # to detect the hand and fingers
    # Use this to flip image
    hands, img = detector.findHands(img, flipType=False)

    img = drawAll(img, buttonList)
    if hands:
        lmList = hands[0]['lmList']

        if lmList:
            for button in buttonList:
                x, y = button.pos
                w, h = button.size
                if x < lmList[8][0] < x+w and y < lmList[8][1] < y+h:
                    cv2.rectangle(img, button.pos,
                                  (x + w, y + h), HOVER, cv2.FILLED)
                    cv2.putText(img, button.text, (x + 18, y + 70),
                                FONT_FAMILY, 4, FONT_COLOR, 4)
                    length, info, img = detector.findDistance(
                        lmList[8], lmList[12], img)

                    if length > CLICK_SIZE:
                        click_released =True
                    # Detect if user clicked,
                    # TODO: create a function if_clicked
                    if length < CLICK_SIZE:
                        # if an app (e.g. notepad) is open the numbers will typed in the app.
                        if button.is_alpha_num:
                            keyboard.press(button.text)
                        elif button.text == 'Exit':
                            exit_pressed = True
                        elif button.text == 'Clear':
                            finalText = ''
                        cv2.rectangle(img, button.pos,
                                      (x + w, y + h), KEY_DIVIDER, cv2.FILLED)

                        cv2.putText(img, button.text, (x + 18, y + 70),
                                    FONT_FAMILY, 4, FONT_COLOR, 4)
                        if click_released:
                            print(F"{button.text} & Click Size= {length}")
                            if button.is_alpha_num:
                                finalText += button.text
                            click_released = False
                        # sleep(0.55)

    # below textbox
    cv2.rectangle(img, (50, 550), (800, 650), HOVER, cv2.FILLED)
    cv2.putText(img, finalText, (60, 600), FONT_FAMILY, 4, FONT_COLOR, 4)

    cv2.imshow("Virtual Keyboard", img)
    cv2.waitKey(1)
