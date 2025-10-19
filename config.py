# Configuration file for Live Stream Setup
# Update these settings according to your Hostinger server details

# Hostinger Server Configuration
HOSTINGER_CONFIG = {
    # Replace with your actual Hostinger domain
    'domain': 'https://your-domain.hostinger.com',
    
    # API endpoints (don't change these unless you modify the server script)
    'api_endpoint': '/stream_server.php/api/stream',
    'status_endpoint': '/stream_server.php/api/status',
    'frame_endpoint': '/stream_server.php/api/get_frame',
    
    # Web app URL
    'web_app_url': '/stream.html',
    
    # Stream identifier (make this unique if you have multiple cameras)
    'stream_id': 'laptop_camera_001'
}

# Camera Configuration
CAMERA_CONFIG = {
    'device_id': 0,  # 0 for default camera, 1 for second camera, etc.
    'width': 640,
    'height': 480,
    'fps': 30,
    'quality': 85  # JPEG quality (1-100)
}

# Network Configuration
NETWORK_CONFIG = {
    'local_port': 5000,  # Port for local monitoring
    'timeout': 5,  # Request timeout in seconds
    'max_retries': 3  # Maximum retry attempts for failed requests
}

# Example configurations for different scenarios:

# For a subdomain setup:
# HOSTINGER_CONFIG['domain'] = 'https://stream.yourdomain.com'

# For a subdirectory setup:
# HOSTINGER_CONFIG['domain'] = 'https://yourdomain.com/livestream'

# For multiple cameras:
# HOSTINGER_CONFIG['stream_id'] = 'laptop_camera_002'  # Different ID for each camera
