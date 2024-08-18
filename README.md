Virtual Dressing Room
Virtual Dressing Room is a real-time application that allows users to try on different shirts using their webcam. Leveraging MediaPipe for pose detection and OpenCV for image processing, this project provides an interactive virtual fitting experience.

Features
Pose Detection: Utilizes MediaPipe to detect body landmarks such as shoulders and hips for accurate shirt placement.
Dynamic Shirt Overlay: Overlays selected shirt images onto the user based on pose landmarks.
Shirt Selection: Cycle through different shirt images with the press of a button.
Screenshot Capture: Save a screenshot of your virtual fitting session.
User Interface: Displays instructions and shirt information on the video feed for ease of use.
Installation
Clone the Repository:

bash
Copy code
git clone https://github.com/yourusername/virtual-dressing-room.git
cd virtual-dressing-room
Install Dependencies:
Ensure you have Python installed, then install the required packages:

bash
Copy code
pip install opencv-python mediapipe numpy
Prepare Shirt Images:
Place your shirt images (PNG with alpha channel for transparency) in the Resources/Shirts directory. Update the shirt_dir variable in the code to point to your shirt images directory.

Usage
Run the Application:

bash
Copy code
python virtual_dressing_room.py
Controls:

n: Change to the next shirt in the list.
s: Save the current frame as a screenshot (screenshot.png).
q: Quit the application.
Code Overview
Initialization: Sets up MediaPipe for pose detection and OpenCV for video capture.
Shirt Overlay: overlay_shirt function adjusts and places the shirt image on the detected pose landmarks.
User Interface: show_gui function displays instructions and shirt information on the video frame.
Main Loop: Captures video frames, detects pose landmarks, applies shirt overlay, and handles user inputs.
Contributing
Feel free to fork the repository, submit issues, or contribute improvements. Contributions and feedback are welcome!
