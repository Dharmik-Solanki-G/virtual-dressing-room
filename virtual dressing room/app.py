import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import os
from PIL import Image
import threading
import time

# Page configuration with custom theme
st.set_page_config(
    page_title="Virtual Dressing Room",
    page_icon="👕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .shirt-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        border: 2px solid transparent;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .shirt-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        border-color: #667eea;
    }
    
    .shirt-card.selected {
        border-color: #667eea;
        background: linear-gradient(135deg, #f5f7ff 0%, #e8edff 100%);
    }
    
    .camera-section {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
    }
    
    .stats-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin: 1rem 0;
    }
    
    .upload-section {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.7rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .camera-frame {
        border: 3px solid #667eea;
        border-radius: 15px;
        padding: 10px;
        background: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize MediaPipe Pose
@st.cache_resource
def load_mediapipe():
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        enable_segmentation=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    mp_drawing = mp.solutions.drawing_utils
    return mp_pose, pose, mp_drawing

mp_pose, pose, mp_drawing = load_mediapipe()

# Initialize session state
if 'shirt_images' not in st.session_state:
    st.session_state.shirt_images = []
if 'shirt_names' not in st.session_state:
    st.session_state.shirt_names = []
if 'selected_shirt_index' not in st.session_state:
    st.session_state.selected_shirt_index = 0
if 'camera_active' not in st.session_state:
    st.session_state.camera_active = False
if 'pose_detected' not in st.session_state:
    st.session_state.pose_detected = False
if 'frames_processed' not in st.session_state:
    st.session_state.frames_processed = 0

def load_default_shirts():
    """Load default shirts from Resources/Shirts directory"""
    shirt_dir = 'Resources/Shirts'
    if os.path.exists(shirt_dir):
        shirt_files = [f for f in os.listdir(shirt_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        for shirt_file in sorted(shirt_files):
            if shirt_file not in st.session_state.shirt_names:
                shirt_path = os.path.join(shirt_dir, shirt_file)
                try:
                    pil_img = Image.open(shirt_path)
                    if pil_img.mode != 'RGBA':
                        pil_img = pil_img.convert('RGBA')
                    
                    shirt_array = np.array(pil_img)
                    shirt_bgra = cv2.cvtColor(shirt_array, cv2.COLOR_RGBA2BGRA)
                    
                    st.session_state.shirt_images.append(shirt_bgra)
                    st.session_state.shirt_names.append(shirt_file)
                except Exception as e:
                    st.error(f"Error loading {shirt_file}: {e}")

def process_uploaded_shirt(uploaded_file):
    """Process uploaded shirt image"""
    try:
        image = Image.open(uploaded_file)
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        shirt_array = np.array(image)
        shirt_bgra = cv2.cvtColor(shirt_array, cv2.COLOR_RGBA2BGRA)
        
        return shirt_bgra, uploaded_file.name
    except Exception as e:
        st.error(f"Error processing uploaded file: {e}")
        return None, None

def overlay_shirt(frame, shirt_img, landmarks):
    """Overlay the shirt on the user's body based on pose landmarks"""
    try:
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]

        shoulder_width = int(np.linalg.norm(
            np.array([left_shoulder.x, left_shoulder.y]) - 
            np.array([right_shoulder.x, right_shoulder.y])
        ) * frame.shape[1] * 1.7)
        
        shirt_height = int(shoulder_width * (shirt_img.shape[0] / shirt_img.shape[1]) * 1.28)

        x_center = int((left_shoulder.x + right_shoulder.x) / 2 * frame.shape[1])
        y_center = int((left_shoulder.y + left_hip.y) / 2 * frame.shape[0])

        angle = -np.degrees(np.arctan2(
            left_shoulder.y - right_shoulder.y, 
            left_shoulder.x - right_shoulder.x
        ))

        shirt_resized = cv2.resize(shirt_img, (shoulder_width, shirt_height))

        M = cv2.getRotationMatrix2D((shoulder_width // 2, shirt_height // 2), angle, 1)
        shirt_rotated = cv2.warpAffine(shirt_resized, M, (shoulder_width, shirt_height))

        x_start = max(0, x_center - shoulder_width // 2)
        y_start = max(0, y_center - shirt_height // 2)

        if (y_start + shirt_height > frame.shape[0] or 
            x_start + shoulder_width > frame.shape[1]):
            return frame

        if shirt_rotated.shape[2] == 4:  # Has alpha channel
            alpha = shirt_rotated[:, :, 3] / 255.0
            overlay = shirt_rotated[:, :, :3]

            for c in range(3):
                frame[y_start:y_start+shirt_height, x_start:x_start+shoulder_width, c] = \
                    (1 - alpha) * frame[y_start:y_start+shirt_height, x_start:x_start+shoulder_width, c] + \
                    alpha * overlay[:, :, c]

        return frame
    except Exception as e:
        return frame

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>👕 Virtual Dressing Room</h1>
        <p>Try on different shirts virtually using AI-powered pose detection!</p>
    </div>
    """, unsafe_allow_html=True)

    # Load default shirts
    if not st.session_state.shirt_images:
        load_default_shirts()

    # Sidebar
    with st.sidebar:
        st.markdown("## 👕 **Shirt Collection**")
        
        # Upload section
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.markdown("### 📤 **Upload New Shirts**")
        uploaded_files = st.file_uploader(
            "Drag and drop shirt images here (PNG with transparent background recommended)",
            type=['png', 'jpg', 'jpeg'],
            accept_multiple_files=True,
            help="💡 Tip: PNG files with transparent backgrounds work best!"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Process uploaded files
        if uploaded_files:
            progress_bar = st.progress(0)
            for i, uploaded_file in enumerate(uploaded_files):
                if uploaded_file.name not in st.session_state.shirt_names:
                    shirt_img, shirt_name = process_uploaded_shirt(uploaded_file)
                    if shirt_img is not None:
                        st.session_state.shirt_images.append(shirt_img)
                        st.session_state.shirt_names.append(shirt_name)
                        st.success(f"✅ Added {shirt_name}")
                progress_bar.progress((i + 1) / len(uploaded_files))
            progress_bar.empty()

        # Stats section
        if st.session_state.shirt_images:
            st.markdown(f"""
            <div class="stats-card">
                <h3>📊 Collection Stats</h3>
                <p><strong>{len(st.session_state.shirt_images)}</strong> shirts available</p>
                <p><strong>{st.session_state.frames_processed}</strong> frames processed</p>
                <p>Status: {'🟢 Pose Detected' if st.session_state.pose_detected else '🔴 No Pose'}</p>
            </div>
            """, unsafe_allow_html=True)

        # Shirt selection
        if st.session_state.shirt_images:
            st.markdown("### 🎽 **Select Your Shirt**")
            
            for i, (shirt_img, shirt_name) in enumerate(zip(st.session_state.shirt_images, st.session_state.shirt_names)):
                selected_class = "selected" if i == st.session_state.selected_shirt_index else ""
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # Convert for display
                    shirt_rgb = cv2.cvtColor(shirt_img, cv2.COLOR_BGRA2RGB)
                    pil_img = Image.fromarray(shirt_rgb)
                    st.image(pil_img, width=80)
                
                with col2:
                    if st.button(f"👕 {shirt_name}", key=f"shirt_{i}", help=f"Click to select {shirt_name}"):
                        st.session_state.selected_shirt_index = i
                        st.success(f"Selected: {shirt_name}")
            
            # Management buttons
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🗑️ Clear All"):
                    st.session_state.shirt_images = []
                    st.session_state.shirt_names = []
                    st.session_state.selected_shirt_index = 0
                    st.rerun()
            
            with col2:
                if st.button("🔄 Refresh"):
                    st.rerun()

    # Main content
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Camera section
        st.markdown('<div class="camera-section">', unsafe_allow_html=True)
        st.markdown("## 📹 **Virtual Try-On Studio**")
        
        # Camera controls
        col_start, col_stop = st.columns(2)
        
        with col_start:
            if st.button("🎥 Start Camera", type="primary", use_container_width=True):
                if st.session_state.shirt_images:
                    st.session_state.camera_active = True
                    st.success("Camera started! Stand in front of the camera.")
                else:
                    st.error("Please upload some shirts first!")
        
        with col_stop:
            if st.button("⏹️ Stop Camera", use_container_width=True):
                st.session_state.camera_active = False
                st.info("Camera stopped.")
        

        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Camera feed
        camera_placeholder = st.empty()
        
        # Instructions
        with st.expander("📋 **How to Use**", expanded=False):
            st.markdown("""
            1. **Upload Shirts**: Use the sidebar to drag and drop shirt images
            2. **Select Shirt**: Click on any shirt from your collection
            3. **Start Camera**: Click the 'Start Camera' button
            4. **Position Yourself**: Stand 3-6 feet from the camera
            5. **Pose Naturally**: Raise your arms slightly for best results
            6. **Try Different Shirts**: Use the sidebar to switch between shirts
            
            **💡 Tips for Best Results:**
            - Use PNG images with transparent backgrounds
            - Ensure good lighting in your room
            - Stand against a plain background
            - Keep your full torso visible in the camera
            """)
    
    with col2:
        # Current selection display
        st.markdown("## 🎯 **Current Selection**")
        
        if st.session_state.shirt_images and st.session_state.selected_shirt_index < len(st.session_state.shirt_images):
            current_shirt = st.session_state.shirt_images[st.session_state.selected_shirt_index]
            current_name = st.session_state.shirt_names[st.session_state.selected_shirt_index]
            
            # Display current shirt with nice styling
            st.markdown('<div class="shirt-card">', unsafe_allow_html=True)
            shirt_rgb = cv2.cvtColor(current_shirt, cv2.COLOR_BGRA2RGB)
            pil_img = Image.fromarray(shirt_rgb)
            st.image(pil_img, caption=f"Selected: {current_name}", use_column_width=True)
            
            st.markdown(f"""
            **👕 Name:** {current_name}  
            **📐 Dimensions:** {current_shirt.shape[1]} × {current_shirt.shape[0]}  
            **🎨 Channels:** {current_shirt.shape[2]}
            """)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No shirt selected. Upload and select a shirt to get started!")
        
        # Performance metrics
        if st.session_state.camera_active:
            st.markdown("## 📊 **Live Stats**")
            stats_placeholder = st.empty()

    # Camera processing loop
    if st.session_state.camera_active and st.session_state.shirt_images:
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            st.error("❌ Could not access camera. Please check permissions.")
            st.session_state.camera_active = False
        else:
            frame_count = 0
            start_time = time.time()
            
            while st.session_state.camera_active:
                ret, frame = cap.read()
                if not ret:
                    st.error("Failed to read from camera")
                    break
                
                # Flip frame for mirror effect
                frame = cv2.flip(frame, 1)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame_rgb)
                
                # Update pose detection status
                st.session_state.pose_detected = results.pose_landmarks is not None
                
                if results.pose_landmarks:
                    landmarks = results.pose_landmarks.landmark
                    current_shirt = st.session_state.shirt_images[st.session_state.selected_shirt_index]
                    frame = overlay_shirt(frame, current_shirt, landmarks)
                    
                    # Optional: Draw pose landmarks
                    # mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                
                # Convert back to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Add frame border and display
                with camera_placeholder.container():
                    st.markdown('<div class="camera-frame">', unsafe_allow_html=True)
                    st.image(frame_rgb, channels="RGB", use_column_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Update stats
                frame_count += 1
                st.session_state.frames_processed += 1
                
                if frame_count % 30 == 0:  # Update stats every 30 frames
                    fps = frame_count / (time.time() - start_time)
                    with stats_placeholder.container():
                        st.metric("FPS", f"{fps:.1f}")
                        st.metric("Frames", st.session_state.frames_processed)
                        st.metric("Pose", "✅ Detected" if st.session_state.pose_detected else "❌ Not Detected")
                
                time.sleep(0.033)  # ~30 FPS
        
        cap.release()

if __name__ == "__main__":
    main()