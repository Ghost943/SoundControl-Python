#Hello , This project made by Ghost943
#This project is a very simple project to control the volume on and off with hand gestures
#And this is my first Github post I'll try to post new stuff 
#GOODBYE :)
"""
This code will only increase the volume by 2 notches. If you want to increase or decrease it more, you can use the following code: 'pyautogui.press("volumeup")' and 'pyautogui.press("volumedown")'. The more you repeat it, the more the volume will be increased or decreased.
"""


import math
import cv2
import mediapipe as mp
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Create a video capture object for the camera
cap = cv2.VideoCapture(0)

# Create a hand tracking pipeline.
hands = mp_hands.Hands()

# Define a threshold distance to control the sound
threshold_distance = 0.1  # Adjust this value as needed

# Set the initial state of the sound control
is_sound_on = False

while True:
    # Read the camera frame
    ret, frame = cap.read()

    # Flip the frame horizontally for a mirror effect
    frame = cv2.flip(frame, 1)

    # Convert the frame to RGB color space
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Start the hand tracking pipeline.
    results = hands.process(frame_rgb)

    # Get the position and orientation of the hands.
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the position of the thumb.
            thumb_position = (
                hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x,
                hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
            )

            # Get the position of the index finger.
            index_finger_position = (
                hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x,
                hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            )

            # Calculate the distance between the thumb and index finger.
            distance = math.sqrt(
                (thumb_position[0] - index_finger_position[0]) ** 2 +
                (thumb_position[1] - index_finger_position[1]) ** 2
            )

            # Change sound state based on distance
            if distance < threshold_distance:
                if not is_sound_on:
                    # Sound is currently off, turn it on
                    pyautogui.press("volumeup")  # Adjust the appropriate key as per your system
                    # Example: if you want to press the space key every time you open and close it, you can change it with the following code
                    is_sound_on = True
            else:
                if is_sound_on:
                    # Sound is currently on, turn it off
                   
                    pyautogui.press("volumedown")  # Adjust the appropriate key as per your system
                    # Example: if you want to press the space key every time you open and close it, you can change it with the following code
                    is_sound_on = False

            # Draw hand landmarks on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display the frame
    cv2.imshow('Hand Tracking', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the windows
cap.release()
cv2.destroyAllWindows()
hands.close()
