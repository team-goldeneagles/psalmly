import requests

def gloo_api(user_input, gloo_api_key):
    # Use the mood in the query for the Gloo API request
    url = f"https://developer.ai.gloo.us/api/search?query={user_input}&num_results=1&threshold=0.5"
    headers = {
        "accept": "application/json",
        "x-api-key": gloo_api_key
    }
    
    # Make the request to the Gloo API
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
        # Extract the 'christiantopics' from the first element in the list
        if data and isinstance(data, list) and 'christiantopics' in data[0]:
            christiantopics = data[0]['christiantopics']
            print(f"Christian Topics: {christiantopics}")
            return christiantopics
        else:
            print("No Christian Topics found")
            return None
    else:
        print(f"Error: {response.status_code}")
        return None