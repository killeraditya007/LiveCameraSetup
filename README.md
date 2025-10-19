# Live Room Camera Stream

A Python-based live streaming solution that allows you to monitor your room from anywhere using your laptop's camera and a web interface.

## Features

- 🎥 Real-time camera streaming using OpenCV
- 🌐 Web-based interface accessible from any device
- 📱 Responsive design that works on desktop and mobile
- 🔄 Automatic camera status monitoring
- 🎛️ Easy start/stop controls
- 📊 Real-time status indicators

## Requirements

- Python 3.7 or higher
- Webcam or built-in camera
- Modern web browser
- Network access (local network or internet)

## Installation

1. **Clone or download this project**
   ```bash
   git clone <your-repo-url>
   cd LiveStreamSetup
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Starting the Server

1. **Run the Python backend server**
   ```bash
   python backend/app.py
   ```

2. **Open your web browser** and navigate to:
   ```
   http://localhost:5000
   ```

3. **Access the web interface** by opening:
   ```
   frontend/index.html
   ```
   Or serve it through a web server for better functionality.

### Using the Web Interface

1. **Start the Camera**: Click the "Start Camera" button to begin streaming
2. **View Live Feed**: The video feed will appear in the main area
3. **Stop Camera**: Click "Stop Camera" to stop streaming
4. **Refresh**: Use "Refresh Feed" if the video stops working

## Network Access

### Local Network Access
To access from other devices on your local network:

1. Find your laptop's IP address:
   - Windows: `ipconfig`
   - Mac/Linux: `ifconfig`

2. Access from other devices using:
   ```
   http://YOUR_IP_ADDRESS:5000
   ```

### Internet Access
To access from anywhere on the internet:

1. **Port Forwarding**: Configure your router to forward port 5000 to your laptop
2. **Dynamic DNS**: Use a service like No-IP or DuckDNS for a consistent domain
3. **Cloud Deployment**: Deploy to services like Heroku, AWS, or DigitalOcean

## Security Considerations

⚠️ **Important Security Notes:**

- This setup is for personal use and testing
- The camera feed is not encrypted by default
- Consider adding authentication for production use
- Be aware of privacy implications when streaming

## Troubleshooting

### Camera Issues
- **Camera not detected**: Make sure no other applications are using the camera
- **Permission denied**: Grant camera permissions to your terminal/IDE
- **Poor quality**: Adjust camera settings in the code

### Network Issues
- **Can't access from other devices**: Check firewall settings
- **Connection refused**: Ensure the server is running and accessible
- **Slow streaming**: Reduce video quality or frame rate in the code

### Common Solutions
1. **Restart the server** if the camera stops working
2. **Check camera permissions** in your system settings
3. **Verify network connectivity** between devices
4. **Update browser** if the web interface doesn't load properly

## Customization

### Video Quality
Edit `backend/app.py` to adjust:
- Frame size: `cv2.CAP_PROP_FRAME_WIDTH` and `cv2.CAP_PROP_FRAME_HEIGHT`
- Frame rate: `cv2.CAP_PROP_FPS`
- JPEG quality: `cv2.IMWRITE_JPEG_QUALITY`

### Styling
Modify `frontend/index.html` to customize:
- Colors and themes
- Layout and responsive design
- Additional features and controls

## File Structure

```
LiveStreamSetup/
├── backend/
│   └── app.py              # Python Flask server
├── frontend/
│   └── index.html          # Web interface
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Dependencies

- **opencv-python**: Camera capture and video processing
- **flask**: Web server framework
- **flask-cors**: Cross-origin resource sharing
- **pillow**: Image processing
- **numpy**: Numerical operations

## License

This project is for educational and personal use. Please respect privacy laws and regulations in your jurisdiction.

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all dependencies are installed correctly
3. Ensure your camera is working with other applications
4. Check network connectivity and firewall settings
