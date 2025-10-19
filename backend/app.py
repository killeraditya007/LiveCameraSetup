import cv2
import base64
import threading
import time
import requests
import json
from flask import Flask, Response, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

# Import configuration
try:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config import HOSTINGER_CONFIG, CAMERA_CONFIG, NETWORK_CONFIG
    
    SERVER_CONFIG = {
        'hostinger_url': HOSTINGER_CONFIG['domain'],
        'api_endpoint': HOSTINGER_CONFIG['api_endpoint'],
        'status_endpoint': HOSTINGER_CONFIG['status_endpoint'],
        'stream_id': HOSTINGER_CONFIG['stream_id']
    }
except ImportError:
    print("Warning: config.py not found. Using default configuration.")
    print("Please create config.py with your Hostinger server details.")
    SERVER_CONFIG = {
        'hostinger_url': 'https://your-domain.hostinger.com',  # Replace with your actual domain
        'api_endpoint': '/stream_server.php/api/stream',
        'status_endpoint': '/stream_server.php/api/status',
        'stream_id': 'laptop_camera_001'
    }

class CameraStream:
    def __init__(self):
        self.camera = None
        self.frame = None
        self.is_streaming = False
        self.lock = threading.Lock()
        self.server_connected = False
        self.stream_thread = None
        
    def start_camera(self):
        """Initialize and start the camera"""
        try:
            # Check server connection first
            if not self.check_server_connection():
                print("Warning: Cannot connect to Hostinger server. Camera will start but streaming may fail.")
            
            # Get camera settings from config
            try:
                device_id = CAMERA_CONFIG['device_id']
                width = CAMERA_CONFIG['width']
                height = CAMERA_CONFIG['height']
                fps = CAMERA_CONFIG['fps']
                quality = CAMERA_CONFIG['quality']
            except NameError:
                # Fallback to defaults if config not available
                device_id = 0
                width = 640
                height = 480
                fps = 30
                quality = 85
            
            self.camera = cv2.VideoCapture(device_id)
            if not self.camera.isOpened():
                raise Exception("Could not open camera")
            
            # Set camera properties for better performance
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            self.camera.set(cv2.CAP_PROP_FPS, fps)
            
            self.is_streaming = True
            
            # Start streaming thread to server
            self.stream_thread = threading.Thread(target=self.stream_to_server, daemon=True)
            self.stream_thread.start()
            
            print("Camera started successfully and streaming to server")
            return True
        except Exception as e:
            print(f"Error starting camera: {e}")
            return False
    
    def stop_camera(self):
        """Stop the camera and release resources"""
        self.is_streaming = False
        if self.camera:
            self.camera.release()
            self.camera = None
        
        # Wait for streaming thread to finish
        if self.stream_thread and self.stream_thread.is_alive():
            self.stream_thread.join(timeout=2)
        
        print("Camera stopped")
    
    def get_frame(self):
        """Capture a frame from the camera"""
        if not self.camera or not self.is_streaming:
            return None
            
        ret, frame = self.camera.read()
        if ret:
            with self.lock:
                self.frame = frame
            return frame
        return None
    
    def get_latest_frame(self):
        """Get the latest captured frame"""
        with self.lock:
            return self.frame.copy() if self.frame is not None else None
    
    def send_frame_to_server(self, frame):
        """Send frame to Hostinger server"""
        try:
            # Get quality setting from config
            try:
                quality = CAMERA_CONFIG['quality']
            except NameError:
                quality = 85
            
            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
            if ret:
                # Convert to base64
                frame_base64 = base64.b64encode(buffer).decode('utf-8')
                
                # Prepare payload
                payload = {
                    'stream_id': SERVER_CONFIG['stream_id'],
                    'frame': frame_base64,
                    'timestamp': time.time()
                }
                
                # Get timeout setting from config
                try:
                    timeout = NETWORK_CONFIG['timeout']
                except NameError:
                    timeout = 5
                
                # Send to server
                response = requests.post(
                    f"{SERVER_CONFIG['hostinger_url']}{SERVER_CONFIG['api_endpoint']}",
                    json=payload,
                    timeout=timeout
                )
                
                if response.status_code == 200:
                    self.server_connected = True
                    return True
                else:
                    print(f"Server responded with status: {response.status_code}")
                    self.server_connected = False
                    return False
        except Exception as e:
            print(f"Error sending frame to server: {e}")
            self.server_connected = False
            return False
    
    def stream_to_server(self):
        """Continuously stream frames to server"""
        while self.is_streaming:
            frame = self.get_frame()
            if frame is not None:
                self.send_frame_to_server(frame)
            time.sleep(0.033)  # ~30 FPS
    
    def check_server_connection(self):
        """Check if server is reachable"""
        try:
            # Get timeout setting from config
            try:
                timeout = NETWORK_CONFIG['timeout']
            except NameError:
                timeout = 5
                
            response = requests.get(
                f"{SERVER_CONFIG['hostinger_url']}{SERVER_CONFIG['status_endpoint']}",
                timeout=timeout
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Server connection check failed: {e}")
            return False

# Global camera stream instance
camera_stream = CameraStream()

def generate_frames():
    """Generate video frames for streaming"""
    while camera_stream.is_streaming:
        frame = camera_stream.get_frame()
        if frame is not None:
            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            if ret:
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(0.033)  # ~30 FPS

@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        'status': 'Live Stream Server Running',
        'camera_status': 'active' if camera_stream.is_streaming else 'inactive'
    })

@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    if not camera_stream.is_streaming:
        return "Camera not started", 500
    
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_camera', methods=['POST'])
def start_camera():
    """Start the camera"""
    if camera_stream.start_camera():
        return jsonify({'status': 'success', 'message': 'Camera started'})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to start camera'}), 500

@app.route('/stop_camera', methods=['POST'])
def stop_camera():
    """Stop the camera"""
    camera_stream.stop_camera()
    return jsonify({'status': 'success', 'message': 'Camera stopped'})

@app.route('/camera_status')
def camera_status():
    """Get camera status"""
    return jsonify({
        'is_streaming': camera_stream.is_streaming,
        'camera_available': camera_stream.camera is not None,
        'server_connected': camera_stream.server_connected,
        'server_url': SERVER_CONFIG['hostinger_url']
    })

@app.route('/server_config')
def server_config():
    """Get server configuration"""
    return jsonify({
        'server_url': SERVER_CONFIG['hostinger_url'],
        'stream_id': SERVER_CONFIG['stream_id'],
        'web_app_url': f"{SERVER_CONFIG['hostinger_url']}/stream.html"
    })

if __name__ == '__main__':
    print("Starting Live Stream Client...")
    print(f"Target server: {SERVER_CONFIG['hostinger_url']}")
    print("Make sure your camera is connected and not being used by other applications")
    print("IMPORTANT: Update SERVER_CONFIG in this file with your actual Hostinger domain!")
    
    # Check server connection
    if camera_stream.check_server_connection():
        print("✓ Successfully connected to Hostinger server")
    else:
        print("✗ Cannot connect to Hostinger server. Please check your configuration.")
    
    # Start camera automatically
    if camera_stream.start_camera():
        print("Camera initialized successfully and streaming to server")
    else:
        print("Warning: Could not initialize camera. You can start it manually via /start_camera endpoint")
    
    # Get local port from config
    try:
        local_port = NETWORK_CONFIG['local_port']
    except NameError:
        local_port = 5000
    
    # Run the Flask app (this is just for local monitoring)
    app.run(host='127.0.0.1', port=local_port, debug=True, threaded=True)
