import cv2
import base64
import threading
import time
from flask import Flask, Response, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

class CameraStream:
    def __init__(self):
        self.camera = None
        self.frame = None
        self.is_streaming = False
        self.lock = threading.Lock()
        
    def start_camera(self):
        """Initialize and start the camera"""
        try:
            self.camera = cv2.VideoCapture(0)  # 0 for default camera
            if not self.camera.isOpened():
                raise Exception("Could not open camera")
            
            # Set camera properties for better performance
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.camera.set(cv2.CAP_PROP_FPS, 30)
            
            self.is_streaming = True
            print("Camera started successfully")
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
        'camera_available': camera_stream.camera is not None
    })

if __name__ == '__main__':
    print("Starting Live Stream Server...")
    print("Make sure your camera is connected and not being used by other applications")
    
    # Start camera automatically
    if camera_stream.start_camera():
        print("Camera initialized successfully")
    else:
        print("Warning: Could not initialize camera. You can start it manually via /start_camera endpoint")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
