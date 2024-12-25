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
# from  prompt_csv_processing import generate_infographics_from_prompt_and_csv
# from gif_animation_creation import create_animated_gif

def convert_gif_to_storytelling_video(gif_path, text):
    """
    Converts a GIF into a storytelling video using imageio
    """
    import os
    from PIL import Image, ImageDraw, ImageFont
    import numpy as np
    import imageio
    
    # Process text for insights
    summary = nlp_pipeline(text, '')
    categories = summary['categories']
    values = summary['values']
    
    def create_text_frame(text, size=(1920, 1080), bg_color='white'):
        img = Image.new('RGB', size, color=bg_color)
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()
        
        # Get text bbox
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center text
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        
        draw.text((x, y), text, fill='black' if bg_color == 'white' else 'white', font=font)
        # Convert to RGB numpy array
        return np.array(img.convert('RGB'))
    
    # Prepare frames
    frames = []
    fps = 30
    
    # 1. Title sequence (2 seconds)
    title_frame = create_text_frame("Market Share Analysis", bg_color='black')
    for _ in range(2 * fps):
        frames.append(title_frame)
    
    # 2. GIF sequence (4 seconds)
    gif = Image.open(gif_path)
    gif_frames = []
    try:
        while True:
            frame = gif.copy()
            # Resize frame and ensure RGB
            frame = frame.convert('RGB').resize((1920, 1080), Image.LANCZOS)
            # Convert to numpy array
            frame_array = np.array(frame)
            gif_frames.append(frame_array)
            gif.seek(len(gif_frames))
    except EOFError:
        pass
    
    # Extend gif frames to 4 seconds
    frames_needed = 4 * fps
    while len(gif_frames) < frames_needed:
        gif_frames.extend(gif_frames)
    frames.extend(gif_frames[:frames_needed])
    
    # 3. Explanation sequence (4 seconds)
    explanations = [
        "Analyzing market share data...",
        f"Main competitor: {categories[values.index(max(values))]} leads with {max(values)}%",
        f"Market gap analysis shows {max(values)-min(values)}% difference",
        f"Total market coverage: {sum(values)}%",
        "Generating insights and recommendations..."
    ]
    
    frames_per_explanation = int((4 * fps) / len(explanations))
    for exp in explanations:
        exp_frame = create_text_frame(exp)
        for _ in range(frames_per_explanation):
            frames.append(exp_frame)
    
    # Verify all frames have same shape and channels
    frame_shape = frames[0].shape
    frames = [frame.reshape(frame_shape) if frame.shape != frame_shape else frame 
             for frame in frames]
    
    # Save as MP4
    output_path = 'data_storytelling_video.mp4'
    
    print("Writing video...")
    writer = imageio.get_writer(output_path, fps=fps)
    for frame in frames:
        writer.append_data(frame)
    writer.close()
    
    print(f"Data storytelling video saved as: {output_path}")
    return output_path
pass