from flask import Flask, request, jsonify
from fitbit.main import RequestHandler
import os
from dotenv import load_dotenv

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
