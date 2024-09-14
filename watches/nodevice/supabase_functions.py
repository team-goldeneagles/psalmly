import requests
import time
import os
from urllib.parse import urlparse, parse_qs
from supabase import create_client, Client

# Initialize Supabase client
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def handle_audio_storage(audio_url, audio_title):
    # Step 1: Parse the original URL to extract the item_id
    parsed_url = urlparse(audio_url)
    query_params = parse_qs(parsed_url.query)
    item_id = query_params.get('item_id', [None])[0]

    # Check if the item_id is found
    if not item_id:
        print("Error: item_id not found in the URL")
        return None

    # Step 2: Reconstruct the correct audio URL
    new_audio_url = f"https://cdn1.suno.ai/{item_id}.mp3"

    # Step 3: Proceed with the download process
    local_filename = f"{audio_title}.mp3"

    attempts = 0
    max_attempts = 3
    downloaded_audio = None
    filename = audio_title.lower().replace(' ', '_') + ".mp3"
    supabase_path = f"psalmly/{filename}"

    while attempts < max_attempts:
        try:
            response = requests.get(new_audio_url, stream=True)
            # response = requests.get("https://cdn1.suno.ai/dafb3640-4020-4b06-812e-96faad3c05ec.mp3", stream=True)
            if response.status_code == 200:
                print("ran download")
                # Download the file
                with open(filename, 'wb+') as f:
                    f.write(response.content)
                downloaded_audio = filename
                break
            else:
                print("failed")
                attempts += 1
                time.sleep(2)  # Delay before retrying
        except Exception as e:
            print(f"Error downloading file: {e}")
            attempts += 1

    if not downloaded_audio:
        print("Failed to download audio after multiple attempts.")
        return ""

    # Upload the file to Supabase
    try:
        with open(filename, 'rb') as f:
            supabase.storage.from_("psalmly").upload(
                file=f,
                path=filename,
                file_options={"content-type": "audio/mpeg"}
            )
        
        return f"https://api.ievangelize.app/storage/v1/object/public/psalmly/psalmly/{filename}"
    except Exception as e:
        print(f"Error uploading to Supabase: {e}")
        return ""