import requests
from .supabase_functions import handle_audio_storage  # Import the new Supabase function
from urllib.parse import urlparse, parse_qs
import time

def generate_music(lyrics, genre, title, aiml_api_key):
    url = "https://api.aimlapi.com/generate/custom-mode"
    headers = {
        "Authorization": f"Bearer {aiml_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": lyrics,
        "tags": genre,
        "title": title,
        "make_instrumental": False,
        "wait_audio": True
    }
    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()
    
    if len(response_json) > 1:
        second_song = response_json[1]
        audio_url = second_song.get("audio_url")
        audio_title = second_song.get("title")

        # Call the Supabase function to handle the audio

        # #########################################
        time.sleep(10)
        parsed_url = urlparse(audio_url)
        query_params = parse_qs(parsed_url.query)
        item_id = query_params.get('item_id', [None])[0]

        temp_url = f"https://api.aimlapi.com/?ids[0]={item_id}"
        temp_response = requests.get(temp_url, headers=headers)
        print(temp_response.text)

        ###############################################

        new_audio_url = handle_audio_storage(audio_url, audio_title)

        return {
            "title": second_song.get("title"),
            "image_url": second_song.get("image_url"),
            "lyrics": second_song.get("lyric"),
            "audio_url": new_audio_url,  # Use the new audio URL from Supabase
            "tags": second_song.get("tags")
        }
    else:
        print("Less than two songs found in the response.")
        return {}