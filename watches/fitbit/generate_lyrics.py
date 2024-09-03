from openai import OpenAI

def generate_lyrics_and_genres(fitbit_data, mood, aiml_api_key):
    lyrics_prompt = f"Generate lyrics for a song that reflects a {mood} mood with the following health data: {fitbit_data}"
    client = OpenAI(
        api_key=aiml_api_key,
        base_url="https://api.aimlapi.com",
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are an expert song Christian writer. You write songs based on someone's mood, mental health and fitbit data to make them feel better. You write good lyrics that are based on scripture. Determine someone's current mood by analyzing the fitbit data.",
            },
            {
                "role": "user",
                "content": lyrics_prompt
            },
        ],
        temperature=1,
        max_tokens=100,
        top_p=0.9,
        frequency_penalty=0.2,
        presence_penalty=0,
    )
    lyrics = response.choices[0].message.content
    genre = "christian music, christian pop, dance"

    return lyrics, genre
