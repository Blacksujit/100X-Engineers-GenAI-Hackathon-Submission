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
# from prompt_csv_processing import generate_infographics_from_prompt_and_csv

def create_detailed_infographic(text):
    """
    Creates a static detailed infographic for data storytelling
    """
    import matplotlib.pyplot as plt
    
    # Process text
    summary = nlp_pipeline(text, '')
    categories = summary['categories']
    values = summary['values']
    
    # Create figure with subplots
    fig = plt.figure(figsize=(15, 10))
    
    # Main bar plot
    ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=2)
    bars = ax1.bar(categories, values, color='skyblue')
    ax1.set_title('Market Share Distribution', fontsize=16)
    ax1.set_ylabel('Percentage (%)')
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}%',
                ha='center', va='bottom')
    
    # Pie chart
    ax2 = plt.subplot2grid((2, 2), (1, 0))
    ax2.pie(values, labels=categories, autopct='%1.1f%%')
    ax2.set_title('Market Share Proportion')
    
    # Additional insights text
    ax3 = plt.subplot2grid((2, 2), (1, 1))
    ax3.axis('off')
    total = sum(values)
    insights_text = f"""Key Insights:
    
    • Total market coverage: {total}%
    • Leading brand: {categories[values.index(max(values))]}
    • Market share gap: {max(values)-min(values)}%
    """
    ax3.text(0, 0.5, insights_text, fontsize=12, va='center')
    
    plt.tight_layout()
    
    # Save high-quality image
    output_path = 'detailed_infographic.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Detailed infographic saved as: {output_path}")
    return output_path
    print(f"Detailed infographic saved as: {output_path}")
    pass