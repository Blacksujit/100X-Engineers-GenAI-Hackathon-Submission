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
from dotenv import load_dotenv
# Hardcoded API keys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, AutoModelForTokenClassification
import gtts  # For text-to-speech audio generation
# from langchain_community import LangChain  # For implementing langchain and other NLP tasks
# from Preprocess_text_NLP import nlp_pipeline
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, AutoModelForTokenClassification
import gtts  # For text-to-speech audio generation
# from langchain_community import LangChain  # For implementing langchain and other NLP tasks
from .text_processing import nlp_pipeline
# from deatil_infographics_creation import create_detailed_infographic


# Define a function to generate infographics from custom prompt and CSV file
def generate_infographics_from_prompt_and_csv(prompt, csv_file):
    # Use the NLP pipeline to process the prompt and CSV file
    summary = nlp_pipeline(prompt, pd.read_csv(csv_file)['Category'].tolist())
    
    # Integrate with AI models like GPT-3 for more dynamic and interactive visualizations
    # Assuming GPT-3 is available and can generate images based on the summary
    # For demonstration, we'll use matplotlib for a simple visualization
    fig, ax = plt.subplots()
    ax.bar(summary['categories'], summary['values'])
    ax.set_title('Infographics from CSV and Prompt')
    ax.set_xlabel('Category')
    ax.set_ylabel('Value')
    plt.savefig('infographics_image.png')
    images = ['infographics_image.png']
    
    # Create a video from the images using moviepy
    from moviepy.editor import ImageSequenceClip
    clip = ImageSequenceClip(images, fps=1)
    clip.write_videofile('infographics_video.mp4')
    pass