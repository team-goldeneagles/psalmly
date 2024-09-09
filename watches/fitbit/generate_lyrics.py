import json
from openai import OpenAI
from .gloo_api import gloo_api

def generate_lyrics_and_genres(fitbit_data, mood, aiml_api_key, gloo_api_key):
    # Call the gloo_api function to get christian topics related to the mood
    christiantopics = gloo_api(mood, gloo_api_key)

    # Construct the lyrics prompt with mood, fitbit data, and christian topics
    lyrics_prompt = f"Question and answers about mood, how I want to feel and music I would prefer to lisen to: {mood}. Here is the fitbit health data: {fitbit_data}."
    
    if christiantopics:
        lyrics_prompt += f" Here are some Christian topics and themes: {christiantopics}"

    client = OpenAI(
        api_key=aiml_api_key,
        base_url="https://api.aimlapi.com",
    )

    try:
      response = client.chat.completions.create(
        # OpenAI API code
      )

      json_output = response.choices[0].message.content
      print(json_output)
      # Add a check if the response is empty or not valid JSON
      if not json_output.strip():
          raise ValueError("Received empty response from OpenAI")

      # Attempt to parse the response as JSON
      song_data = json.loads(json_output)
      title = song_data.get("Title", "Untitled")
      genres = song_data.get("Genres", "Unknown")
      lyrics = song_data.get("Lyrics", "No lyrics available")

  except json.JSONDecodeError as e:
      print(f"JSONDecodeError: {e}")
      return "Error: Invalid JSON response", "Unknown genre"
  
  except Exception as e:
      print(f"Error: {e}")
      return "Error: Unable to generate lyrics", "Unknown genre"

  return lyrics, genres, title