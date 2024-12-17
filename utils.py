print("Loading utils.py from app/")
import requests
import time
print("Loading utils.py from app/")
from dotenv import load_dotenv
# Hardcoded API keys
# PEXELS_API_KEY = ''
import os

load_dotenv()

PEXELS_API_KEY = os.environ.get('PEXELS_API_KEY')

# Text processing functions
def parse_input_text(text):
    data_points = {}
    parts = text.split(',')
    for part in parts:
        part = part.strip()
        if '%' in part:
            key, value = part.split('%')
            data_points[key.strip()] = float(value.strip().replace('%', '')) / 100
        else:
            try:
                key_value = part.split(' ', 1)
                if len(key_value) == 2:
                    key, value = key_value
                    data_points[key.strip()] = value.strip()
                else:
                    try:
                        data_points[part] = float(part)
                    except ValueError:
                        print(f"Could not parse part: '{part}'")
            except ValueError:
                print(f"Could not parse part: '{part}'")
                continue
    return data_points


# text processing functions
def preprocess_text(text):
    return text.strip()


# video Generation Function
def generate_video_from_text(text):
    processed_prompt = preprocess_text(text)
    visualization_prompt = f"Create an animated infographic video showing the distribution of: {processed_prompt}"

    headers = {'Authorization': PEXELS_API_KEY}
    params = {'query': f'infographics {visualization_prompt}', 'per_page': 5}

    time.sleep(3)
    response = requests.get('https://api.pexels.com/videos/search', headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Pexels API request failed with status code {response.status_code}")

    try:
        videos = response.json().get('videos', [])
    except Exception as e:
        raise Exception("Invalid JSON response from Pexels API.")
    
    video_urls = [video['video_files'][0]['link'] for video in videos if video['video_files']]
    
    time.sleep(3)
    return video_urls[:3]
