<?php
// Hostinger Server Script - Live Stream Relay
// Upload this file to your Hostinger server's public_html directory

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
    exit(0);
}

// Configuration
$STREAM_DATA_FILE = 'stream_data.json';
$MAX_FRAME_AGE = 10; // seconds - frames older than this are considered stale

// Function to get current timestamp
function getCurrentTime() {
    return time();
}

// Function to save stream data
function saveStreamData($streamId, $frameData, $timestamp) {
    global $STREAM_DATA_FILE;
    
    $data = [
        'stream_id' => $streamId,
        'frame' => $frameData,
        'timestamp' => $timestamp,
        'server_time' => getCurrentTime()
    ];
    
    // Save to file (in production, consider using a database)
    file_put_contents($STREAM_DATA_FILE, json_encode($data));
    return true;
}

// Function to get latest stream data
function getLatestStreamData() {
    global $STREAM_DATA_FILE, $MAX_FRAME_AGE;
    
    if (!file_exists($STREAM_DATA_FILE)) {
        return null;
    }
    
    $data = json_decode(file_get_contents($STREAM_DATA_FILE), true);
    
    if (!$data) {
        return null;
    }
    
    // Check if frame is too old
    $age = getCurrentTime() - $data['timestamp'];
    if ($age > $MAX_FRAME_AGE) {
        return null; // Frame is stale
    }
    
    return $data;
}

// Handle different endpoints
$request_uri = $_SERVER['REQUEST_URI'];
$path = parse_url($request_uri, PHP_URL_PATH);

// Remove leading slash and get the endpoint
$endpoint = ltrim($path, '/');

switch ($endpoint) {
    case 'api/stream':
        // Handle incoming stream data from laptop
        if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
            http_response_code(405);
            echo json_encode(['error' => 'Method not allowed']);
            exit;
        }
        
        $input = json_decode(file_get_contents('php://input'), true);
        
        if (!$input || !isset($input['stream_id']) || !isset($input['frame'])) {
            http_response_code(400);
            echo json_encode(['error' => 'Invalid data']);
            exit;
        }
        
        $streamId = $input['stream_id'];
        $frameData = $input['frame'];
        $timestamp = isset($input['timestamp']) ? $input['timestamp'] : getCurrentTime();
        
        if (saveStreamData($streamId, $frameData, $timestamp)) {
            echo json_encode(['status' => 'success', 'message' => 'Frame received']);
        } else {
            http_response_code(500);
            echo json_encode(['error' => 'Failed to save frame']);
        }
        break;
        
    case 'api/status':
        // Handle status check
        $data = getLatestStreamData();
        $isActive = $data !== null;
        
        echo json_encode([
            'status' => 'online',
            'stream_active' => $isActive,
            'server_time' => getCurrentTime(),
            'last_frame_time' => $isActive ? $data['timestamp'] : null
        ]);
        break;
        
    case 'api/get_frame':
        // Handle frame requests from web app
        $data = getLatestStreamData();
        
        if ($data) {
            echo json_encode([
                'status' => 'success',
                'frame' => $data['frame'],
                'timestamp' => $data['timestamp'],
                'stream_id' => $data['stream_id']
            ]);
        } else {
            http_response_code(404);
            echo json_encode(['error' => 'No active stream']);
        }
        break;
        
    default:
        // Default response
        echo json_encode([
            'message' => 'Live Stream Server API',
            'endpoints' => [
                'POST /api/stream' => 'Receive stream data from laptop',
                'GET /api/status' => 'Check server and stream status',
                'GET /api/get_frame' => 'Get latest frame for web app'
            ],
            'server_time' => getCurrentTime()
        ]);
        break;
}
?>
