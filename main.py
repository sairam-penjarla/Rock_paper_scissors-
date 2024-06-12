import cv2
import random
import mediapipe as mp
from utils import get_gesture, puttext

class RockPaperScissorsGame:
    def __init__(self):
        """
        Initialize the RockPaperScissorsGame class.
        """
        self.options = ['Rock', 'Paper', 'Scissors']
        self.last_pos = "None"
        self.FONT_SIZE = 6
        self.FONT_THICKNESS = 6
    def run(self):
        """
        Main method to run the Rock Paper Scissors game.
        """
        # Open the video capture device
        cap = cv2.VideoCapture(0)

        # Initialize the hand tracking module
        with mp.solutions.hands.Hands(
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as hands:
            # Loop until the video capture device is opened
            while cap.isOpened():
                # Read a frame from the video capture device
                success, image = cap.read()

                # Flip the image horizontally for intuitive hand tracking
                image = cv2.flip(image, 1)

                # Convert the image from BGR to RGB format
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                # Process the image to detect hand landmarks
                results = hands.process(image)

                # Make the image writable again
                image.flags.writeable = True

                # Convert the image back to BGR format for display
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # Handle hand landmarks detection results
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        lmList = []
                        for id, lm in enumerate(hand_landmarks.landmark):
                            h, w, c = image.shape
                            cx, cy = int(lm.x * w), int(lm.y * h)
                            lmList.append([id, cx, cy])
                        res = get_gesture(lmList)
                        if res != self.last_pos:
                            ans = self.options[random.randint(0, len(self.options) - 1)]
                            self.last_pos = res
                        cv2.putText(image, ("You: "+ str(res)), (600, 200), cv2.FONT_HERSHEY_PLAIN, self.FONT_SIZE, (0, 0, 0), self.FONT_THICKNESS+2)
                        cv2.putText(image, ("You: "+ str(res)), (600, 200), cv2.FONT_HERSHEY_PLAIN, self.FONT_SIZE, (255, 255, 255),self.FONT_THICKNESS)
                        cv2.putText(image, ("CPU: "+ str(ans)), (60, 100), cv2.FONT_HERSHEY_PLAIN, self.FONT_SIZE, (0, 0, 0), self.FONT_THICKNESS+2)
                        cv2.putText(image, ("CPU: "+ str(ans)), (60, 100), cv2.FONT_HERSHEY_PLAIN, self.FONT_SIZE, (255, 0, 255),self.FONT_THICKNESS)
                        cv2.putText(image, str(puttext(res,ans)), (100, 400), cv2.FONT_HERSHEY_PLAIN, self.FONT_SIZE, (0, 0, 0), self.FONT_THICKNESS+2)
                        cv2.putText(image, str(puttext(res, ans)), (100, 400), cv2.FONT_HERSHEY_PLAIN, self.FONT_SIZE,(255, 0, 255), self.FONT_THICKNESS)

                # Display the image with hand landmarks
                cv2.imshow('MediaPipe Hands', image)

                # Check for the key press event
                if (cv2.waitKey(5) & 0xFF == 27):
                    break

            # Release the video capture device and close all windows
            cap.release()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    game = RockPaperScissorsGame()
    game.run()
