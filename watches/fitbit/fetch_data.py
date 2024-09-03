import requests
from concurrent.futures import ThreadPoolExecutor

def fetch_fitbit_data(url, headers):
    response = requests.get(url, headers=headers)
    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except ValueError as json_err:
        print(f"JSON decode error occurred: {json_err}")
        print("Response content:", response.text)
    return {}

def process_fitbit_data(access_token, date):
    base_urls = {
        "activity": f"https://api.fitbit.com/1/user/-/activities/date/{date}.json",
        "azm": f"https://api.fitbit.com/1/user/-/activities/active-zone-minutes/date/{date}/1d.json",
        "breathing_rate": f"https://api.fitbit.com/1/user/-/br/date/{date}.json",
        "hrv": f"https://api.fitbit.com/1/user/-/hrv/date/{date}.json",
        "heart_rate": f"https://api.fitbit.com/1/user/-/activities/heart/date/{date}/1d.json",
        "sleep": f"https://api.fitbit.com/1.2/user/-/sleep/date/{date}.json"
    }

    headers = {'Authorization': f'Bearer {access_token}'}

    with ThreadPoolExecutor() as executor:
        futures = {label: executor.submit(fetch_fitbit_data, url, headers) for label, url in base_urls.items()}
        results = {label: future.result() for label, future in futures.items()}

    return results
