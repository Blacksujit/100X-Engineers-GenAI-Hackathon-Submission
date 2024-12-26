import os
from PIL import Image
import matplotlib.pyplot as plt
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
print("routes module is being imported")
from .text_processing import nlp_pipeline
print("gif_animation_creation module is being imported")

def create_animated_gif(text):   
    # Use the NLP pipeline to process the text
    summary = nlp_pipeline(text, '')
    categories = summary['categories']
    values = summary['values']
    
    # Create frames directory
    frames_dir = 'animation_frames'
    os.makedirs(frames_dir, exist_ok=True)
    
    def create_frame(frame_number, value_multiplier, categories=categories, values=values):  # Pass values as parameter
        fig, ax = plt.subplots(figsize=(12, 7))
        
        # Calculate current height of bars
        current_values = [v * value_multiplier for v in values]
        
        # Create bars with current height
        bars = ax.bar(categories, current_values, color='skyblue')
        
        # Styling
        ax.set_title('Market Share Analysis', fontsize=20, pad=20)
        ax.set_xlabel('Brands', fontsize=14)
        ax.set_ylabel('Percentage (%)', fontsize=14)
        ax.set_ylim(0, max(values) * 1.2)
        
        # Add value labels
        for bar, value in zip(bars, current_values):
            if value > 0:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(value)}%',
                       ha='center', va='bottom', fontsize=12)
        
        ax.grid(True, axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        # Save frame
        frame_path = os.path.join(frames_dir, f'frame_{frame_number:03d}.png')
        plt.savefig(frame_path, dpi=300, bbox_inches='tight')
        plt.close()
        return frame_path
    
    # Generate frames
    frames = []
    num_frames = 20  # Number of frames for animation
    
    print("Generating frames...")
    for i in range(num_frames + 1):
        multiplier = i / num_frames
        frame_path = create_frame(i, multiplier)
        frames.append(frame_path)
    
    # Create GIF
    print("Creating GIF...")
    images = [Image.open(f) for f in frames]
    
    gif_path = 'animated_infographic.gif'
    images[0].save(
        gif_path,
        save_all=True,
        append_images=images[1:],
        duration=100,  # 100ms between frames
        loop=0
    )
    
    # Clean up frames
    for frame in frames:
        os.remove(frame)
    os.rmdir(frames_dir)
    
    print(f"Animation saved as GIF: {gif_path}")
    return gif_path
pass