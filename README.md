# virtual_keybard
It draws numbers 1 to 9 as buttons on the screen. This app utilizes computer vision (mediapipe, cvzone) to detect the user's hand and fingers in the webcam's image.
When the user's index finger is on the virtual button on the screen, the button's colour changes to dark yellow.
When the user shortens the distance between its index and middle finger by moving the fingers towards each other, the code considers it as a click. The app then writes the number corresponding to the button on the box and on any preferred in the focused app.
 

I am open to any suggestions and changes in the app.
## install:
1. mediapipe version: 0.8.7
2. cvzone version: 1.5.3

## Runtime
* webcam: 
  * if you want to use your laptop webcame change the line:
    * cap = cv2.VideoCapture(IRIUN_WEBCAM, cv2.CAP_DSHOW) to
    * cap = cv2.VideoCapture(DEFAULT_WEBCAM, cv2.CAP_DSHOW)
  * I used Iriun app to turn my phone camera to the webcam. Also it is possible to use XSPLIT app.

* Click Detection:
  * You can adjust the click precision by modifying the CLICK_SIZE = 45 
    * If it does not detect your click increase the number e.g 60 and 70 
    * If it detects too much decrease the number e.g. 30 or 25
    



