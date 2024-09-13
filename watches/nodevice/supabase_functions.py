import requests
import time
import os
from supabase import create_client, Client

# Initialize Supabase client
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def handle_audio_storage(audio_url, audio_title):
    attempts = 0
    max_attempts = 3
    downloaded_audio = None
    filename = audio_title.lower().replace(' ', '_')
    supabase_path = f"psalmly/{filename}"

    while attempts < max_attempts:
        try:
            response = requests.get(audio_url)
            if response.status_code == 200:
                # Download the file
                with open(filename, 'wb+') as f:
                    f.write(response.content)
                downloaded_audio = filename
                break
            else:
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
                path=supabase_path,
                file_options={"content-type": "audio/mpeg"}
            )
        return f"https://https://api.ievangelize.app/storage/v1/object/public/{supabase_path}"
    except Exception as e:
        print(f"Error uploading to Supabase: {e}")
        return ""