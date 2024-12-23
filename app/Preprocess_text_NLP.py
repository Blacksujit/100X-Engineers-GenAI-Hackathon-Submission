import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, AutoModelForTokenClassification
import gtts  # For text-to-speech audio generation
# from langchain_community import LangChain  # For implementing langchain and other NLP tasks



def nlp_pipeline(text, data):
    # Use T5 for summarization
    summary_model = AutoModelForSeq2SeqLM.from_pretrained('t5-base')
    summary_tokenizer = AutoTokenizer.from_pretrained('t5-base')
    
    # Prepare input
    input_text = f"summarize: {text} {data}"
    inputs = summary_tokenizer.encode(input_text, return_tensors='pt', max_length=512, truncation=True)
    
    # Generate summary
    outputs = summary_model.generate(inputs, max_length=100)
    summary_text = summary_tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract percentages and categories using simpler regex patterns
    import re
    percentages = [int(x.strip('%')) for x in re.findall(r'\d+%', text)]
    words = text.split()
    categories = []
    
    # Find words after "use" or "uses"
    for i, word in enumerate(words):
        if word.lower() in ['use', 'uses'] and i + 1 < len(words):
            categories.append(words[i + 1])
    
    if not percentages or not categories:
        percentages = [100]
        categories = ['Summary']
    
    # Generate audio
    tts = gtts.gTTS(summary_text, lang='en')
    tts.save('summary_audio.mp3')
    
    return {
        'categories': categories,
        'values': percentages,
        'text': summary_text
    }