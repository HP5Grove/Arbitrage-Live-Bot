import requests


def get_sports_odds(api_key):
    url = f"https://api.the-odds-api.com/v4/sports/upcoming/odds/?regions=au&markets=h2h&apiKey={api_key}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")
