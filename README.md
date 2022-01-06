# virtual_keybard
It draws numbers 1 to 9 as buttons on the screen. This app utilizes computer vision (mediapipe, cvzone) to detect the user's hand and fingers in the webcam's image. When the user moves index and middle finger near to each other the code considers it as a click. and print the relative button value on the screen and on any preferred in focus app.
I am open to any suggestions and changes in the app.

## install:
1. mediapipe 0.8.7
2. cvzone version 1.5.3

## TODO:
* decide the size of click based the size of hand 
  * e.g: when hand is near the webcam, the size is larger and the size of click is larger 
   e.g.: click = finger size /2 
* change all Id's to pep8 and snake_case

