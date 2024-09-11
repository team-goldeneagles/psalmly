import sys
import os
from dotenv import load_dotenv

# Add the 'watches' directory to the system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fitbit.main import handle_request as handle_fitbit_request
from nodevice.main import handle_request as handle_nodevice_request
from flask import Flask, request, jsonify

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route('/generate_music', methods=['POST'])
def generate_music_route():
    data = request.json
    device = data.get("device")
    access_token = data.get('ACCESS_TOKEN')
    date = data.get('date')
    mood = data.get('mood')
    user_input = data.get('user_input')
    aiml_api_key = os.getenv('AIML_API_KEY')
    gloo_api_key = os.getenv("GLOO_API_KEY")

    # Decide which handler to use based on the device type
    if device == "fitbit":
        output = handle_fitbit_request(fitbit_data, mood, aiml_api_key, gloo_api_key)
    else:
        output = handle_nodevice_request(user_input, aiml_api_key, gloo_api_key)

    return jsonify(output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)