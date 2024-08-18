import cv2
import mediapipe as mp
import numpy as np
import os

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Initialize MediaPipe Drawing for visualizing pose landmarks
mp_drawing = mp.solutions.drawing_utils

# Load Shirt Images from the specified directory
shirt_dir = 'C:\\Users\\dharm\\Desktop\\python\\virtual dressing room\\Resources\\Shirts'
# Load all PNG images with an alpha channel (for transparency) from the directory
shirt_images = [cv2.imread(os.path.join(shirt_dir, img), cv2.IMREAD_UNCHANGED) for img in os.listdir(shirt_dir)]
shirt_index = 0  # Initialize the index for selecting the current shirt

# Capture video from webcam
cap = cv2.VideoCapture(0)

# Function to overlay the shirt on the user's body based on pose landmarks
def overlay_shirt(frame, shirt_img, landmarks):
    # Get shoulder and hip landmarks from the pose detection results
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]

    # Calculate the width of the shirt based on the distance between the shoulders, enlarged by 20%
    shoulder_width = int(np.linalg.norm(np.array([left_shoulder.x, left_shoulder.y]) - 
                                        np.array([right_shoulder.x, right_shoulder.y])) * frame.shape[1] * 1.7)
    # Calculate the height of the shirt based on the aspect ratio of the original image
    shirt_height = int(shoulder_width * (shirt_img.shape[0] / shirt_img.shape[1]) * 1.28)

    # Calculate the center position (x, y) to place the shirt based on shoulder and hip positions
    x_center = int((left_shoulder.x + right_shoulder.x) / 2 * frame.shape[1])
    y_center = int((left_shoulder.y + left_hip.y) / 2 * frame.shape[0])

    # Calculate the rotation angle of the shirt based on the angle between the shoulders
    angle = -np.degrees(np.arctan2(left_shoulder.y - right_shoulder.y, left_shoulder.x - right_shoulder.x))

    # Resize the shirt image to match the calculated dimensions
    try:
        shirt_img = cv2.resize(shirt_img, (shoulder_width, shirt_height))
    except Exception as e:
        print(f"Error resizing shirt: {e}")
        return frame  # Return the original frame if resizing fails

    # Rotate the shirt image according to the calculated tilt angle
    M = cv2.getRotationMatrix2D((shoulder_width // 2, shirt_height // 2), angle, 1)
    shirt_img = cv2.warpAffine(shirt_img, M, (shoulder_width, shirt_height))

    # Calculate the top-left corner where the shirt image will be placed
    x_start = x_center - shoulder_width // 2
    y_start = y_center - shirt_height // 2

    # Ensure the coordinates are within the frame boundaries
    x_start = max(0, x_start)
    y_start = max(0, y_start)

    # Ensure the shirt image fits within the frame boundaries
    if y_start + shirt_height > frame.shape[0] or x_start + shoulder_width > frame.shape[1]:
        print("Shirt dimensions exceed frame boundaries.")
        return frame  # Return the original frame if the shirt exceeds frame boundaries

    # Extract the alpha channel and the RGB color channels from the shirt image
    alpha = shirt_img[:, :, 3] / 255.0
    overlay = shirt_img[:, :, :3]

    # Blend the shirt image with the frame using the alpha channel for transparency
    for c in range(0, 3):
        frame[y_start:y_start+shirt_height, x_start:x_start+shoulder_width, c] = \
            (1 - alpha) * frame[y_start:y_start+shirt_height, x_start:x_start+shoulder_width, c] + \
            alpha * overlay[:, :, c]

    return frame  # Return the frame with the shirt overlaid

# Function to display the GUI elements on the frame
def show_gui(frame, shirt_images, shirt_index):
    # Display instructions for the user
    cv2.putText(frame, "Press 'n' to change shirt, 's' to save image", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    # Display the current shirt number out of the total number of shirts
    cv2.putText(frame, f"Shirt: {shirt_index + 1}/{len(shirt_images)}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

# Main loop to process video frames and apply the virtual dressing room effects
while cap.isOpened():
    ret, frame = cap.read()  # Read a frame from the webcam
    if not ret:
        print("Failed to grab frame.")
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert the frame to RGB for MediaPipe processing
    results = pose.process(frame_rgb)  # Process the frame to detect pose landmarks

    if results.pose_landmarks:  # If pose landmarks are detected
        landmarks = results.pose_landmarks.landmark  # Get the landmarks
        try:
            frame = overlay_shirt(frame, shirt_images[shirt_index], landmarks)  # Overlay the shirt onto the frame
        except Exception as e:
            print(f"Error during overlay: {e}")

        # Draw pose landmarks on the frame for reference
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    show_gui(frame, shirt_images, shirt_index)  # Show the GUI elements (instructions and current shirt)

    cv2.imshow('Virtual Dressing Room', frame)  # Display the frame with the virtual dressing room

    # Handle user inputs
    key = cv2.waitKey(1) & 0xFF
    if key == ord('n'):  # Press 'n' to change to the next shirt
        shirt_index = (shirt_index + 1) % len(shirt_images)
    elif key == ord('s'):  # Press 's' to save the current frame as a screenshot
        cv2.imwrite('screenshot.png', frame)
    elif key == ord('q'):  # Press 'q' to quit the application
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
