import requests
import time
import requests  # Ensure requests is imported
from textblob import TextBlob
import spacy
import moviepy
import  nltk
import os
from datetime import datetime
import json

# Hardcoded API keys
PEXELS_API_KEY = 'yepFtS82dEUPX41sHUOMVzris34EohIYvW8Czo5Z5s6KQ2WHPPe4eIQA'

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

    # Additional processing to convert data points into relevant information
    relevant_info = {}
    for key, value in data_points.items():
        if isinstance(value, float):
            relevant_info[key] = f"{value * 100}%"
        else:
            relevant_info[key] = value

    return relevant_info


def preprocess_text(text):
    cleaned_text = text.strip().lower()
    cleaned_text = ' '.join(sorted(set(cleaned_text.split()), key=lambda x: cleaned_text.index(x)))
    return cleaned_text


def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity


def semantic_segment_transformation(text):
    contextual_prompt = f"Contextual prompt based on: {text}"
    return contextual_prompt



# Video Generation Function
def generate_video_from_text(text):
    contextual_prompt = semantic_segment_transformation(text)
    processed_prompt = preprocess_text(contextual_prompt)
    visualization_prompt = f"Create an animated infographic video showing the distribution of: {processed_prompt}"

    headers = {'Authorization': PEXELS_API_KEY}
    params = {'query': f'infographics {visualization_prompt}', 'per_page': 5}

    time.sleep(3)
    response = requests.get('https://api.pexels.com/videos/search', headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Pexels API request failed with status code {response.status_code}")

    videos = response.json().get('videos', [])
    video_urls = [video['video_files'][0]['link'] for video in videos if video['video_files']]
    
    time.sleep(3)
    return video_urls[:3]


# Log types
LOG_TYPE_GPT = "GPT"
LOG_TYPE_PEXEL = "PEXEL"

# log directory paths
DIRECTORY_LOG_GPT = ".logs/gpt_logs"
DIRECTORY_LOG_PEXEL = ".logs/pexel_logs"

# method to log response from pexel and openai
def log_response(log_type, query,response):
    log_entry = {
        "query": query,
        "response": response,
        "timestamp": datetime.now().isoformat()
    }
    if log_type == LOG_TYPE_GPT:
        if not os.path.exists(DIRECTORY_LOG_GPT):
            os.makedirs(DIRECTORY_LOG_GPT)
        filename = '{}_gpt3.txt'.format(datetime.now().strftime("%Y%m%d_%H%M%S"))
        filepath = os.path.join(DIRECTORY_LOG_GPT, filename)
        with open(filepath, "w") as outfile:
            outfile.write(json.dumps(log_entry) + '\n')

    if log_type == LOG_TYPE_PEXEL:
        if not os.path.exists(DIRECTORY_LOG_PEXEL):
            os.makedirs(DIRECTORY_LOG_PEXEL)
        filename = '{}_pexel.txt'.format(datetime.now().strftime("%Y%m%d_%H%M%S"))
        filepath = os.path.join(DIRECTORY_LOG_PEXEL, filename)
        with open(filepath, "w") as outfile:
            outfile.write(json.dumps(log_entry) + '\n')