import requests
from urllib.parse import urlparse, parse_qs
import time
import asyncio

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
    init_response_json = response.json()
    
    if len(init_response_json) > 1:
        second_song = init_response_json[1]
        audio_url = second_song.get("audio_url")
        new_audio_url = None

        # #########################################
        parsed_url = urlparse(audio_url)
        query_params = parse_qs(parsed_url.query)
        item_id = query_params.get('item_id', [None])[0]

        temp_url = f"https://api.aimlapi.com/?ids[0]={item_id}"

        for attempt in range(10):  # Loop 10 times
            temp_response = requests.get(temp_url, headers=headers)
            response_json = temp_response.json()
            
            # Check if the response status is 'complete'
            if response_json and response_json[0].get('status') == 'complete':
                new_audio_url = response_json[0].get('audio_url')
                break

            # Wait for 15 seconds before the next attempt
            time.sleep(15)


        return {
            "title": second_song.get("title"),
            "image_url": second_song.get("image_url"),
            "lyrics": second_song.get("lyric"),
            "audio_url": second_song.get("audio_url"),
            "tags": second_song.get("tags")
        }
    else:
        print("Less than two songs found in the response.")
        return {}