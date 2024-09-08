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

    response = client.chat.completions.create(
      model="gpt-4o",
      messages=[
        {
          "role": "system",
          "content": [
            {
              "type": "text",
              "text": "You're an expert songwriter. Your lyrics are based on bible verses, scripture and Christian themes.\n- The user will with information about how they feel.\n- That information includes questions and answer about their current mood, how they want to be made to feel and the type of music they would want to listen to.\n- The other information provided by the user is health data, from Fitbit (activity data, active zone minutes, breathing rate data, heart rate data, heart rate data, sleep data )and apple watch, for the past 24 hours.\n- There also be Christian themes in the user input, to help do your job better\n\n# Determining the song title\n- Generate one good short songs title, no longer than 5 words\n\n# Determining the genres\n- The category of music you should produce is Contemporary Christian music category\n- So you should have at least one of the following genres: \"christian music\", \"christian pop\", \"contemporary christian\"\n- Here are genres to pull from as well: \"soft rock\", \"dance\", \"acoustic worship\", \"pop\", \"\"\n\n# Use first person when writing the lyrics\n\n# Explaining user input\n- The user provides very precise information, so you job is to give the output using the stated output format.\n\n# Length of song\n- Song should be between 2 - 4 mins\n\nHere is the format of the output you produce (always do JSON format):\n{\n\"Title\":\"\",\n\"Genres\":\"\",\n\"Lyrics\":\"\"\n}\n\n# Limitations\n- Never deviate from the stated output\n- The output is always JSON format\n- Genre should always be output like  this, \"genre1, genre2, genre3\", so no quotation marks on each genre but instead the whole list"
            },
          ]
        },
        {
          "role": "user",
          "content": [
            {
              "text": lyrics_prompt,
              "type": "text"
            }
          ]
        }
      ],
      temperature=1,
      max_tokens=500,
      top_p=0.9,
      frequency_penalty=0.2,
      presence_penalty=0,
      response_format={
        "type": "text"
      }
    )

    # Extract the JSON output from the response
    json_output = response.choices[0].message.content

    # Parse the JSON output
    song_data = json.loads(json_output)

    # Extract the Title, Genres, and Lyrics from the JSON
    title = song_data.get("Title", "Untitled")
    genre = song_data.get("Genres", "christian music, contemporary christian")
    lyrics = song_data.get("Lyrics", "")

    return lyrics, genre, title
