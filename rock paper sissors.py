import cv2
import mediapipe as mp
import math
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import emoji
import random
import time
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hand_mpDraw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
drawing_spec_dots = mp_drawing.DrawingSpec(color = (201,194,2),thickness=1, circle_radius=2)
drawing_spec_line = mp_drawing.DrawingSpec(color = (255,255,255),thickness=2, circle_radius=1)
options = ['Rock', 'paper', 'scissors']
NewValue = 0
last_pos = "None"
ans = "None"

FONT_SIZE = 6
FONT_THICKNESS = 6

def get_gesture(lmList):
            distance_between_index_finger_and_wrist = int(
                math.hypot(lmList[0][1] - lmList[8][1], lmList[0][2] - lmList[8][2]))
            distance_between_ring_finger_and_wrist = int(
                math.hypot(lmList[16][1] - lmList[0][1], lmList[16][2] - lmList[0][2]))
            if (distance_between_index_finger_and_wrist > 250) and (distance_between_ring_finger_and_wrist > 250):
                return "paper"
            elif (distance_between_index_finger_and_wrist > 250) and (distance_between_ring_finger_and_wrist < 250):
                return "scissors"
            else:
                return "Rock"
def puttext(user_action,computer_action):
    if user_action == computer_action:
        return ("It's a tie!")
    elif user_action == "Rock":
        if computer_action == "scissors":
            return ("You win!")
        else:
            return ("You lose.")
    elif user_action == "paper":
        if computer_action == "Rock":
            return ("You win!")
        else:
            return ("You lose.")
    elif user_action == "scissors":
        if computer_action == "paper":
            return ("You win!")
        else:
            return ("You lose.")
def motor():
    global options, last_pos
    cap = cv2.VideoCapture(0)
    i = 0
    booler = False
    with mp_hands.Hands(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            success, image = cap.read()
            image = cv2.flip(image, 1)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = hands.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    lmList = []
                    for id, lm in enumerate(hand_landmarks.landmark):
                        h, w, c = image.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        lmList.append([id, cx, cy])
                        #tips = [0, 4, 8, 12, 16, 20]
                        #if id in tips:
                            #cv2.circle(image, (cx, cy), 15, (255, 255, 255), cv2.FILLED)
                    #mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS,landmark_drawing_spec=hand_mpDraw.DrawingSpec(color=(0, 0, 0)),connection_drawing_spec=hand_mpDraw.DrawingSpec(color=(201, 194, 2)))
                    res = get_gesture(lmList)
                    if res != last_pos:
                        ans = options[random.randint(0, len(options) - 1)]
                        last_pos = res
                    cv2.putText(image, ("You: "+ str(res)), (600, 200), cv2.FONT_HERSHEY_PLAIN, FONT_SIZE, (0, 0, 0), FONT_THICKNESS+2)
                    cv2.putText(image, ("You: "+ str(res)), (600, 200), cv2.FONT_HERSHEY_PLAIN, FONT_SIZE, (255, 255, 255),FONT_THICKNESS)
                    cv2.putText(image, ("CPU: "+ str(ans)), (60, 100), cv2.FONT_HERSHEY_PLAIN, FONT_SIZE, (0, 0, 0), FONT_THICKNESS+2)
                    cv2.putText(image, ("CPU: "+ str(ans)), (60, 100), cv2.FONT_HERSHEY_PLAIN, FONT_SIZE, (255, 0, 255),FONT_THICKNESS)
                    cv2.putText(image, str(puttext(res,ans)), (100, 400), cv2.FONT_HERSHEY_PLAIN, FONT_SIZE, (0, 0, 0), FONT_THICKNESS+2)
                    cv2.putText(image, str(puttext(res, ans)), (100, 400), cv2.FONT_HERSHEY_PLAIN, FONT_SIZE,(255, 0, 255), FONT_THICKNESS)
            cv2.imshow('MediaPipe Hands', image)
            if (cv2.waitKey(5) & 0xFF == 27):
                break
        cap.release()
        cv2.destroyAllWindows()
motor()