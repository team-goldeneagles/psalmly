import requests

def generate_music(lyrics, genre, aiml_api_key):
    url = "https://api.aimlapi.com/generate/custom-mode"
    headers = {
        "Authorization": f"Bearer {aiml_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": lyrics,
        "tags": genre,
        "title": "First Testing Song",
        "make_instrumental": False,
        "wait_audio": True
    }
    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()
    
    if len(response_json) > 1:
        second_song = response_json[1]
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
