from flask import Flask, jsonify, request
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS  # Enable CORS for React frontend

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow requests from your React frontend

# Spotify API credentials
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

# Spotify API endpoints
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

# Store access token (for simplicity, use a global variable)
access_token = None

@app.route('/')
def index():
    return "Flask API is running!"

@app.route('/login')
def login():
    # Redirect user to Spotify authorization page
    scope = 'user-read-private user-read-email'
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True
    }
    auth_url = f"{AUTH_URL}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"
    return jsonify({'auth_url': auth_url})

@app.route('/callback')
def callback():
    global access_token
    # Handle the callback from Spotify
    if 'error' in request.args:
        return jsonify({'error': request.args['error']}), 400

    if 'code' in request.args:
        # Exchange the authorization code for an access token
        code = request.args['code']
        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
        response = requests.post(TOKEN_URL, data=payload)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data['access_token']
            return jsonify({'message': 'Login successful', 'access_token': access_token})
        else:
            return jsonify({'error': 'Failed to retrieve access token'}), 400
    else
      return jsonify({"message": "error xD"})
@app.route('/search')
def search():
    global access_token
    query = request.args.get('q')
    if query and access_token:
        headers = {'Authorization': f'Bearer {access_token}'}
        params = {'q': query, 'type': 'track', 'limit': 5}
        response = requests.get(f'{API_BASE_URL}search', headers=headers, params=params)
        if response.status_code == 200:
            search_results = response.json()
            return jsonify(search_results)
        else:
            return jsonify({'error': 'Failed to search tracks'}), 400
    return jsonify({'error': 'Missing query or access token'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)