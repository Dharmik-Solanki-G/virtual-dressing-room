import os
import cvzone
import cv2
from cvzone.PoseModule import PoseDetector
import numpy as np

def overlay_image_alpha(img, img_overlay, pos, alpha_mask):
    try:
        x, y = pos
        y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
        x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])
        y1o, y2o = max(0, -y), min(img_overlay.shape[0], img.shape[0] - y)
        x1o, x2o = max(0, -x), min(img_overlay.shape[1], img.shape[1] - x)

        if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
            print("Overlay dimensions invalid, skipping overlay")
            return img

        img_slice = img[y1:y2, x1:x2]
        overlay_slice = img_overlay[y1o:y2o, x1o:x2o]
        alpha = alpha_mask[y1o:y2o, x1o:x2o, np.newaxis] / 255.0
        img[y1:y2, x1:x2] = (1.0 - alpha) * img_slice + alpha * overlay_slice
        print("Overlay applied successfully")
    except Exception as e:
        print(f"Error in overlay_image_alpha: {e}")
    return img

def overlay_shirt(img, lm11, lm12, shirt_img):
    try:
        angle = np.arctan2(lm12[1] - lm11[1], lm12[0] - lm11[0])
        angle_deg = np.degrees(angle)
        print(f"Shoulder angle: {angle_deg:.2f} degrees")

        midpoint = ((lm11[0] + lm12[0]) // 2, (lm11[1] + lm12[1]) // 2)
        print(f"Midpoint between shoulders: {midpoint}")

        shoulder_distance = np.linalg.norm(np.array(lm12) - np.array(lm11))
        print(f"Shoulder distance: {shoulder_distance:.2f}")

        original_shirt_width = shirt_img.shape[1]
        scale_factor = shoulder_distance / original_shirt_width * 2.5  # Increased scale factor
        print(f"Scale factor: {scale_factor:.2f}")

        resized_shirt = cv2.resize(shirt_img, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_AREA)
        print(f"Resized shirt shape: {resized_shirt.shape}")

        center_of_shirt = (resized_shirt.shape[1] // 2, resized_shirt.shape[0] // 2)
        M = cv2.getRotationMatrix2D(center_of_shirt, angle_deg, 1.0)
        rotated_shirt = cv2.warpAffine(resized_shirt, M, (resized_shirt.shape[1], resized_shirt.shape[0]), flags=cv2.INTER_LINEAR)

        # Adjust vertical position to place shirt below shoulders
        vertical_adjustment = int(rotated_shirt.shape[0] * 0.2)  # Reduced vertical adjustment
        shirt_position = [
            int(midpoint[0] - rotated_shirt.shape[1] // 2),
            int(midpoint[1] - vertical_adjustment)  # Place shirt below shoulder midpoint
        ]
        
        # Clip the shirt position to ensure it's within the image boundaries
        shirt_position[0] = max(0, min(shirt_position[0], img.shape[1] - rotated_shirt.shape[1]))
        shirt_position[1] = max(0, min(shirt_position[1], img.shape[0] - rotated_shirt.shape[0]))
        
        print(f"Adjusted shirt position: {shirt_position}")

        if rotated_shirt.shape[2] == 4:
            alpha_mask = rotated_shirt[:, :, 3]
            rotated_shirt = rotated_shirt[:, :, :3]
        else:
            alpha_mask = np.ones(rotated_shirt.shape[:2], dtype=np.uint8) * 255

        img = overlay_image_alpha(img, rotated_shirt, tuple(shirt_position), alpha_mask)
        print("Shirt overlay completed")

        # Debug: Draw landmarks and shirt outline
        cv2.circle(img, tuple(lm11), 5, (0, 255, 0), -1)  # Left shoulder
        cv2.circle(img, tuple(lm12), 5, (0, 255, 0), -1)  # Right shoulder
        cv2.rectangle(img, tuple(shirt_position), 
                      (shirt_position[0] + rotated_shirt.shape[1], shirt_position[1] + rotated_shirt.shape[0]), 
                      (0, 255, 0), 2)  # Shirt outline
    except Exception as e:
        print(f"Error in overlay_shirt: {e}")
    return img

# Initialize video capture and pose detector
try:
    cap = cv2.VideoCapture(r"Resources\Videos\1.mp4")
    if not cap.isOpened():
        raise Exception("Could not open video file")
    print("Video capture initialized successfully")
except Exception as e:
    print(f"Error initializing video capture: {e}")
    exit()

detector = PoseDetector()

# Load shirt images
shirtFolderPath = "Resources/Shirts"
try:
    listShirts = os.listdir(shirtFolderPath)
    if not listShirts:
        raise Exception("No shirts found in the specified folder")
    print(f"Found {len(listShirts)} shirts")
except Exception as e:
    print(f"Error loading shirt images: {e}")
    exit()

imageNumber = 0
imgButtonRight = cv2.imread("Resources/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)
counterRight = 0
counterLeft = 0
selectionSpeed = 10

frame_count = 0
while True:
    try:
        success, img = cap.read()
        if not success:
            print("Failed to read the video frame")
            break

        frame_count += 1
        print(f"Processing frame {frame_count}")

        img = detector.findPose(img)
        lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)

        if lmList:
            print("Pose detected")
            lm11 = lmList[11][1:3]  # Left shoulder
            lm12 = lmList[12][1:3]  # Right shoulder
            print(f"Left shoulder: {lm11}, Right shoulder: {lm12}")

            imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)
            if imgShirt is None:
                print(f"Failed to load shirt image: {listShirts[imageNumber]}")
                continue

            img = overlay_shirt(img, lm11, lm12, imgShirt)

            img = cvzone.overlayPNG(img, imgButtonRight, (1074, 293))
            img = cvzone.overlayPNG(img, imgButtonLeft, (72, 293))

            if lmList[16][1] < 300:
                counterRight += 1
                cv2.ellipse(img, (139, 360), (66, 66), 0, 0, counterRight * selectionSpeed, (0, 255, 0), 20)
                if counterRight * selectionSpeed > 360:
                    counterRight = 0
                    if imageNumber < len(listShirts) - 1:
                        imageNumber += 1
                        print(f"Switched to shirt {imageNumber}")
            elif lmList[15][1] > 900:
                counterLeft += 1
                cv2.ellipse(img, (1138, 360), (66, 66), 0, 0, counterLeft * selectionSpeed, (0, 255, 0), 20)
                if counterLeft * selectionSpeed > 360:
                    counterLeft = 0
                    if imageNumber > 0:
                        imageNumber -= 1
                        print(f"Switched to shirt {imageNumber}")
            else:
                counterRight = 0
                counterLeft = 0
        else:
            print("No pose detected in this frame")

        cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("User quit the program")
            break
    except Exception as e:
        print(f"Error in main loop: {e}")

cap.release()
cv2.destroyAllWindows()
print("Program ended")
