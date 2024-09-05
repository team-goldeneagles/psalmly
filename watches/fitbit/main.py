import os
from dotenv import load_dotenv
from .generate_music import generate_music  # Use relative imports
from .fetch_data import process_fitbit_data
from .generate_lyrics import generate_lyrics_and_genres

# Load environment variables from the .env file
load_dotenv()

class RequestHandler:
    def __init__(self, access_token, date, mood, aiml_api_key):
        self.access_token = access_token
        self.date = date
        self.mood = mood
        self.aiml_api_key = aiml_api_key

    def handle_request(self):
        fitbit_data = process_fitbit_data(self.access_token, self.date)
        lyrics, genre = generate_lyrics_and_genres(fitbit_data, self.mood, self.aiml_api_key)
        music_info = generate_music(lyrics, genre, self.aiml_api_key)
        return music_info

if __name__ == "__main__":
    access_token = os.getenv("ACCESS_TOKEN")
    date = "2024-03-17"
    mood = "I feel depressed and feel lonely. I need encouragement that God loves and sees me."
    aiml_api_key = os.getenv("AIML_API_KEY")

    handler = RequestHandler(access_token, date, mood, aiml_api_key)
    output = handler.handle_request()
    print(output)
