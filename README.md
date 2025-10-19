# Live Room Camera Stream with Hostinger Server

A Python-based live streaming solution that uses your Hostinger server as a relay to stream your laptop camera feed, allowing you to monitor your room from anywhere in the world.

## Features

- 🎥 Real-time camera streaming using OpenCV
- 🌐 Web-based interface accessible from anywhere on the internet
- 📱 Responsive design that works on desktop and mobile
- 🔄 Automatic camera status monitoring
- 🎛️ Easy start/stop controls
- 📊 Real-time status indicators
- 🚀 Hostinger server integration for global access
- 🔒 Secure streaming through your own server

## Requirements

- Python 3.7 or higher
- Webcam or built-in camera
- Modern web browser
- Hostinger hosting account (or any PHP-enabled web hosting)
- Internet connection on both laptop and viewing device

## Installation

### Step 1: Setup Hostinger Server

1. **Upload server files to Hostinger:**
   - Upload `server/stream_server.php` to your Hostinger's `public_html` directory
   - Upload `server/stream.html` to your Hostinger's `public_html` directory

2. **Test server setup:**
   - Visit `https://your-domain.hostinger.com/stream_server.php` to verify the API is working
   - Visit `https://your-domain.hostinger.com/stream.html` to see the web interface

### Step 2: Setup Laptop Client

1. **Clone or download this project**
   ```bash
   git clone <your-repo-url>
   cd LiveStreamSetup
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your server details:**
   - Edit `config.py` and update the `HOSTINGER_CONFIG['domain']` with your actual Hostinger domain
   - Optionally adjust camera and network settings

## Usage

### Starting the Stream

1. **Run the Python client on your laptop**
   ```bash
   python backend/app.py
   ```

2. **The client will automatically:**
   - Connect to your Hostinger server
   - Start your laptop camera
   - Begin streaming video to the server

3. **Access the live feed from anywhere:**
   - Open your browser and go to: `https://your-domain.hostinger.com/stream.html`
   - The web interface will automatically connect and display your live camera feed

### Using the Web Interface

1. **Automatic Connection**: The web app automatically connects to your stream
2. **View Live Feed**: Your laptop camera feed appears in real-time
3. **Status Monitoring**: See server and stream status at the bottom
4. **Refresh**: Use "Refresh Stream" if the video stops working

### Local Monitoring (Optional)

You can also monitor the stream locally by visiting:
```
http://localhost:5000
```
This shows the client status and allows manual camera control.

## How It Works

### Architecture
```
Laptop Camera → Python Client → Hostinger Server → Web Browser (Anywhere)
```

1. **Laptop**: Python client captures video from your camera
2. **Hostinger Server**: Receives video frames and stores them temporarily
3. **Web Browser**: Fetches latest frames from server and displays them
4. **Global Access**: Anyone with the URL can view your stream from anywhere

### Network Flow
- Your laptop sends video frames to your Hostinger server via HTTPS
- The server stores the latest frame and serves it to web browsers
- Multiple people can view the stream simultaneously
- No port forwarding or complex network setup required

## Security Considerations

⚠️ **Important Security Notes:**

- This setup is for personal use and testing
- The camera feed is transmitted over HTTPS to your server
- Consider adding authentication for production use
- Be aware of privacy implications when streaming
- Your Hostinger server acts as a relay - ensure it's secure
- Consider adding password protection to the web interface

## Troubleshooting

### Camera Issues
- **Camera not detected**: Make sure no other applications are using the camera
- **Permission denied**: Grant camera permissions to your terminal/IDE
- **Poor quality**: Adjust camera settings in `config.py`

### Server Connection Issues
- **Cannot connect to Hostinger**: Check your domain in `config.py`
- **Server not responding**: Verify `stream_server.php` is uploaded correctly
- **API errors**: Check Hostinger error logs

### Streaming Issues
- **No video feed**: Ensure laptop client is running and connected
- **Delayed video**: Normal for internet streaming, adjust quality in config
- **Stream stops**: Check internet connection on laptop

### Common Solutions
1. **Restart the laptop client** if streaming stops
2. **Check camera permissions** in your system settings
3. **Verify Hostinger server files** are uploaded correctly
4. **Test server API** by visiting the PHP file directly
5. **Check internet connection** on both laptop and viewing device

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
│   └── app.py              # Python client (runs on laptop)
├── server/
│   ├── stream_server.php   # Server script (upload to Hostinger)
│   └── stream.html         # Web interface (upload to Hostinger)
├── frontend/
│   └── index.html          # Local web interface (optional)
├── config.py               # Configuration file
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

### Hostinger Files
Upload these files to your Hostinger `public_html` directory:
- `server/stream_server.php` → `public_html/stream_server.php`
- `server/stream.html` → `public_html/stream.html`

## Dependencies

### Python Dependencies (Laptop)
- **opencv-python**: Camera capture and video processing
- **flask**: Local web server for monitoring
- **flask-cors**: Cross-origin resource sharing
- **pillow**: Image processing
- **numpy**: Numerical operations
- **requests**: HTTP requests to Hostinger server

### Server Requirements (Hostinger)
- **PHP 7.0+**: For the server script
- **File write permissions**: To store temporary stream data
- **HTTPS support**: For secure streaming

## Configuration Options

### Camera Settings (`config.py`)
```python
CAMERA_CONFIG = {
    'device_id': 0,      # Camera device (0 = default)
    'width': 640,        # Video width
    'height': 480,       # Video height
    'fps': 30,           # Frames per second
    'quality': 85        # JPEG quality (1-100)
}
```

### Network Settings (`config.py`)
```python
NETWORK_CONFIG = {
    'local_port': 5000,  # Local monitoring port
    'timeout': 5,        # Request timeout
    'max_retries': 3     # Retry attempts
}
```

## Advanced Setup

### Multiple Cameras
To stream from multiple laptops:
1. Use different `stream_id` values in each laptop's `config.py`
2. Modify the web interface to select which stream to view

### Custom Domain
If you have a custom domain on Hostinger:
1. Update `HOSTINGER_CONFIG['domain']` in `config.py`
2. Ensure SSL certificate is active

### Authentication
For added security, consider:
1. Adding password protection to the web interface
2. Implementing API key authentication
3. Using HTTPS for all communications

## License

This project is for educational and personal use. Please respect privacy laws and regulations in your jurisdiction.

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify Hostinger server files are uploaded correctly
3. Test the server API endpoints directly
4. Check camera permissions and internet connectivity
5. Review Hostinger error logs if available
