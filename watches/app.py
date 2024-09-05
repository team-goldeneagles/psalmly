import sys
import os
from dotenv import load_dotenv

# Add the 'watches' directory to the system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fitbit.main import RequestHandler
from flask import Flask, request, jsonify

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route('/generate_music', methods=['POST'])
def generate_music_route():
    data = request.json
    access_token = os.getenv('ACCESS_TOKEN')
    date = data.get('date')
    mood = data.get('mood')
    aiml_api_key = os.getenv('AIML_API_KEY')

    handler = RequestHandler(access_token, date, mood, aiml_api_key)
    output = handler.handle_request()

    return jsonify(output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
