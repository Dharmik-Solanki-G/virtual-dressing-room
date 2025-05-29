# 👕 Virtual Dressing Room

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Try on different shirts virtually using AI-powered pose detection!**

[Demo](#-demo) • [Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Contributing](#-contributing)

</div>

## 🎯 Overview

Virtual Dressing Room is an innovative AI-powered application that allows users to try on different shirts virtually using real-time pose detection. Built with Streamlit, OpenCV, and MediaPipe, it provides an interactive and engaging experience for virtual fashion try-ons.

## ✨ Features

### 🎨 **Modern Interactive UI**
- **Beautiful gradient design** with smooth animations
- **Drag-and-drop interface** for easy shirt uploads
- **Real-time statistics** and performance monitoring
- **Responsive layout** that works on all screen sizes

### 🤖 **AI-Powered Technology**
- **MediaPipe pose detection** for accurate body tracking
- **Real-time shirt overlay** with proper scaling and rotation
- **Automatic pose alignment** for natural shirt fitting
- **30 FPS processing** for smooth real-time experience

### 👕 **Smart Shirt Management**
- **Visual shirt collection** with thumbnail previews
- **One-click shirt switching** during live sessions
- **Support for multiple formats** (PNG, JPG, JPEG)
- **Transparent background support** for realistic overlays

### 📱 **User Experience**
- **Mirror effect camera** for natural interaction
- **Live pose detection feedback** with status indicators
- **Performance metrics** showing FPS and processing stats
- **Intuitive controls** with clear visual feedback

## 🎬 Demo

### Screenshots

**Main Interface**
```
┌─────────────────────────────────────────────────────────────┐
│  👕 Virtual Dressing Room                                   │
│  Try on different shirts virtually using AI-powered pose!   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────┐  ┌─────────────────────────────────────────┐
│ 👕 Shirt        │  │ 📹 Virtual Try-On Studio               │
│ Collection      │  │                                         │
│                 │  │ [🎥 Start Camera] [⏹️ Stop Camera]     │
│ 📤 Upload       │  │                                         │
│ New Shirts      │  │ ┌─────────────────────────────────────┐ │
│                 │  │ │                                     │ │
│ 🎽 Select       │  │ │        Live Camera Feed            │ │
│ Your Shirt      │  │ │                                     │ │
│                 │  │ └─────────────────────────────────────┘ │
│ 📊 Stats        │  └─────────────────────────────────────────┘
│ 5 shirts        │
│ 1,250 frames    │
│ 🟢 Pose Detected│
└─────────────────┘
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Webcam/Camera access
- 4GB+ RAM recommended

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Dharmik-Solanki-G/virtual-dressing-room.git
   cd virtual-dressing-room
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL manually

### Alternative Installation

Using conda:
```bash
conda create -n virtual-dressing python=3.9
conda activate virtual-dressing
pip install -r requirements.txt
streamlit run app.py
```

## 📖 Usage

### Getting Started

1. **Launch the Application**
   ```bash
   streamlit run app.py
   ```

2. **Upload Your Shirts**
   - Use the sidebar drag-and-drop interface
   - Upload PNG files with transparent backgrounds for best results
   - Supported formats: PNG, JPG, JPEG

3. **Select a Shirt**
   - Click on any shirt thumbnail in the collection
   - Preview appears in the "Current Selection" section

4. **Start Virtual Try-On**
   - Click "🎥 Start Camera"
   - Position yourself 3-6 feet from the camera
   - Raise your arms slightly for better pose detection

5. **Try Different Shirts**
   - Switch shirts in real-time using the sidebar
   - No need to stop the camera

### 💡 Tips for Best Results

- **Lighting**: Ensure good, even lighting in your room
- **Background**: Stand against a plain, contrasting background
- **Distance**: Stay 3-6 feet away from the camera
- **Pose**: Keep your full torso visible, arms slightly raised
- **Images**: Use PNG files with transparent backgrounds
- **Resolution**: Higher resolution shirts (500x500+) work better

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Space` | Toggle camera on/off |
| `N` | Next shirt |
| `P` | Previous shirt |

## 🛠️ Technical Details

### Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │    MediaPipe    │    │     OpenCV      │
│   Frontend      │───▶│  Pose Detection │───▶│ Image Processing│
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       ▼                       │
         │              ┌─────────────────┐              │
         └─────────────▶│  Shirt Overlay  │◀─────────────┘
                        │    Algorithm    │
                        └─────────────────┘
```

### Key Components

- **Pose Detection**: MediaPipe for real-time body landmark detection
- **Image Processing**: OpenCV for shirt overlay and transformations
- **UI Framework**: Streamlit for interactive web interface
- **State Management**: Session state for real-time updates

### Performance Optimizations

- **Cached model loading** to reduce initialization time
- **Optimized frame processing** at 30 FPS
- **Efficient memory management** for large shirt collections
- **Asynchronous camera handling** for smooth UI updates

## 📁 Project Structure

```
virtual-dressing-room/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── LICENSE               # MIT License
├── Resources/            # Default shirt collection
│   ├── Shirts/          # Shirt image files
│   │   ├── 1.png
│   │   ├── 2.png
│   │   └── ...
│   └── pose_tracking_full_body_landmarks.png
```

## 🔧 Configuration

### Camera Settings
```python
# In app.py, modify these parameters:
CAMERA_INDEX = 0          # Change if using external camera
FPS_TARGET = 30           # Adjust based on your hardware
DETECTION_CONFIDENCE = 0.5 # Lower for more sensitive detection
```

### Shirt Overlay Settings
```python
# Adjust shirt fitting parameters:
SHIRT_WIDTH_MULTIPLIER = 1.7    # Shirt width scaling
SHIRT_HEIGHT_MULTIPLIER = 1.28  # Shirt height scaling
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Reporting Issues
- Use the [GitHub Issues](https://github.com/Dharmik-Solanki-G/virtual-dressing-room/issues) page
- Include detailed steps to reproduce
- Attach screenshots if applicable

### Feature Requests
- Check existing issues first
- Describe the feature and its benefits
- Consider implementation complexity

### Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/Dharmik-Solanki-G/virtual-dressing-room.git
cd virtual-dressing-room

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest tests/

# Format code
black app.py
```

## 🐛 Troubleshooting

### Common Issues

**Camera Not Working**
```bash
# Check camera permissions
# Try different camera index (0, 1, 2...)
# Restart the application
```

**Poor Pose Detection**
- Improve lighting conditions
- Stand further from camera
- Ensure full body is visible
- Check camera resolution

**Shirt Not Overlaying Properly**
- Use PNG images with transparent backgrounds
- Ensure shirt images are high quality
- Adjust shirt scaling parameters

**Performance Issues**
- Close other applications using camera
- Reduce FPS_TARGET in configuration
- Use smaller shirt image files

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 4GB | 8GB+ |
| CPU | Dual-core 2GHz | Quad-core 3GHz+ |
| Camera | 720p | 1080p |
| OS | Windows 10/macOS 10.14/Ubuntu 18.04 | Latest versions |

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **MediaPipe** team for the amazing pose detection library
- **Streamlit** for the fantastic web app framework
- **OpenCV** community for computer vision tools
- All contributors and users who help improve this project

## 🔗 Links

- **Repository**: [GitHub](https://github.com/Dharmik-Solanki-G/virtual-dressing-room)
- **Issues**: [Bug Reports](https://github.com/Dharmik-Solanki-G/virtual-dressing-room/issues)
- **Discussions**: [Community](https://github.com/Dharmik-Solanki-G/virtual-dressing-room/discussions)
- **Documentation**: [Wiki](https://github.com/Dharmik-Solanki-G/virtual-dressing-room/wiki)

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/Dharmik-Solanki-G/virtual-dressing-room?style=social)
![GitHub forks](https://img.shields.io/github/forks/Dharmik-Solanki-G/virtual-dressing-room?style=social)
![GitHub issues](https://img.shields.io/github/issues/Dharmik-Solanki-G/virtual-dressing-room)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Dharmik-Solanki-G/virtual-dressing-room)

---

<div align="center">

**Made with ❤️ by [Dharmik Solanki](https://github.com/Dharmik-Solanki-G)**

⭐ Star this repository if you found it helpful!

</div>