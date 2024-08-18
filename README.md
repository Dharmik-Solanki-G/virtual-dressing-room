Virtual Dressing Room
Virtual Dressing Room is a real-time application that lets users try on different shirts using their webcam. It employs MediaPipe for pose detection and OpenCV for image processing.

Features
Pose Detection: Detects key body landmarks to accurately overlay shirts.
Shirt Selection: Easily switch between multiple shirt images.
Screenshot Capture: Save screenshots of your virtual fitting sessions.
User Interface: Displays instructions and current shirt information.
Installation
Clone the Repository:

bash
Copy code
git clone https://github.com/Dharmik-Solanki-G/virtual-dressing-room.git
cd virtual-dressing-room
Install Dependencies:
Ensure you have Python installed, then install the required packages:

bash
Copy code
pip install opencv-python mediapipe numpy
Prepare Shirt Images:

Place PNG images with transparency in the Resources/Shirts directory.
Update the shirt_dir variable in app.py to point to your directory.
Usage
Run the Application:

bash
Copy code
python app.py
Controls:

n: Change to the next shirt.
s: Save the current frame as a screenshot (screenshot.png).
q: Quit the application.
Contributing
Contributions are welcome! Feel free to fork the repository, open issues, or submit pull requests.

License
This project is licensed under the MIT License.

