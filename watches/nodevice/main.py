import os
from dotenv import load_dotenv
from .generate_music import generate_music  # Use relative imports
from .generate_lyrics import generate_lyrics_and_genres

# Load environment variables from the .env file
load_dotenv()

class RequestHandler:
    def __init__(self, user_input, aiml_api_key, gloo_api_key):
        self.user_input = user_input
        self.aiml_api_key = aiml_api_key
        self.gloo_api_key = gloo_api_key  # Include Gloo API key


    def handle_request(self):
        # Generate lyrics and genre, title, passing the gloo_api_key if necessary
        lyrics, genre, title = generate_lyrics_and_genres(self.user_input, self.aiml_api_key, self.gloo_api_key)
        
        # Generate music based on lyrics and genre
        music_info = generate_music(lyrics, genre, title, self.aiml_api_key)
        return music_info

if __name__ == "__main__":
    user_input = "I feel depressed and feel lonely. I need encouragement that God loves and sees me."
    aiml_api_key = os.getenv("AIML_API_KEY")
    gloo_api_key = os.getenv("GLOO_API_KEY")

    # Pass gloo_api_key to the handler
    handler = RequestHandler(user_input, aiml_api_key, gloo_api_key)
    output = handler.handle_request()
