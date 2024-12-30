"""
This script imports the necessary libraries for a comprehensive data processing, visualization, and video generation pipeline.
Libraries:
- pandas: Data manipulation and analysis.
- numpy: Numerical operations.
- seaborn: Statistical data visualization.
- sklearn.model_selection: Splitting data into training and testing sets.
- sklearn.preprocessing: Standardizing features.
- sklearn.linear_model: Implementing linear regression models.
- sklearn.metrics: Evaluating model performance.
- pandas.read_csv, pandas.read_excel: Reading data from CSV and Excel files.
- scipy.stats: Statistical functions.
- moviepy.editor: Video editing and creation.
- gtts: Text-to-speech conversion.
- matplotlib.pyplot: Plotting graphs and charts.
"""
# Loading necessary Libraries

import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from pandas import read_csv, read_excel
from scipy import stats
# from moviepy.editor import VideoClip, concatenate_videoclips, VideoFileClip, AudioFileClip, ImageSequenceClip
from gtts import gTTS
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import os
import pickle
import requests
import time
import json
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, AutoModelForTokenClassification
import re
import shutil
from PIL import Image, ImageDraw, ImageFont
import imageio
import uuid
from diffusers import DiffusionPipeline
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from pandas import read_csv, read_excel
from scipy import stats
from moviepy.editor import VideoClip, concatenate_videoclips, VideoFileClip, AudioFileClip, ImageSequenceClip
from gtts import gTTS
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import os
import pickle
import requests
import time
import json
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import re
import shutil
from PIL import Image, ImageDraw, ImageFont
import imageio
import uuid
# Loading all The necessary Libraries
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from pandas import read_csv, read_excel
from scipy import stats
from moviepy.editor import VideoClip, concatenate_videoclips
from gtts import gTTS
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import os
from matplotlib.animation import FuncAnimation
from scipy.signal import savgol_filter
from time import perf_counter
import math
# from config_loader import load_config_ani, load_config_setup
import matplotlib.pyplot as plt
import os
import pickle
import gtts
import requests
import time
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, AutoModelForTokenClassification
from moviepy.editor import VideoFileClip, AudioFileClip, ImageSequenceClip
import re
import shutil
from PIL import Image, ImageDraw, ImageFont
import imageio
import uuid
from transformers import pipeline, T5ForConditionalGeneration, T5TokenizerFast
import re
import os
import uuid
import gtts
from textblob import TextBlob
from langdetect import detect
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from pandas import read_csv, read_excel
from scipy import stats
from moviepy.editor import VideoClip, concatenate_videoclips, VideoFileClip, AudioFileClip, ImageSequenceClip
from gtts import gTTS
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import os
import pickle
import requests
import time
import json
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, AutoModelForTokenClassification
import re
import shutil
from PIL import Image, ImageDraw, ImageFont
import imageio
import uuid
from diffusers import DiffusionPipeline
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from pandas import read_csv, read_excel
from scipy import stats
from moviepy.editor import VideoClip, concatenate_videoclips, VideoFileClip, AudioFileClip, ImageSequenceClip, TextClip, CompositeVideoClip
from gtts import gTTS
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import os
import pickle
import requests
import time
import json
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import re
import shutil
from PIL import Image, ImageDraw, ImageFont
import imageio
import uuid
import logging
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from pandas import read_csv, read_excel
from scipy import stats
from moviepy.editor import VideoClip, concatenate_videoclips, VideoFileClip, AudioFileClip, ImageSequenceClip, TextClip, CompositeVideoClip, ImageClip
from gtts import gTTS
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import os
import pickle
import requests
import time
import json
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import re
import shutil
from PIL import Image, ImageDraw, ImageFont
import imageio
import uuid
import logging
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from pandas import read_csv, read_excel
from scipy import stats
from gtts import gTTS
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import os
import pickle
import requests
import time
import json
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import re
import shutil
from PIL import Image, ImageDraw, ImageFont
import imageio
import uuid
import logging
from tqdm import tqdm
# from manim import *
import gtts
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from langdetect import detect
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from langdetect import detect
from tqdm import tqdm
import os



# Set the HF_HOME environment variable to change the cache path
os.environ['HF_HOME'] = "D:\\cahc_models_folder"  # Change this to your desired cache path

# Load the model and tokenizer from .pkl files
models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')

with open(os.path.join(models_dir, 'model.pkl'), 'rb') as model_file:
    summary_model = pickle.load(model_file)

with open(os.path.join(models_dir, 'tokenizer.pkl'), 'rb') as tokenizer_file:
    summary_tokenizer = pickle.load(tokenizer_file)


# Initialize sentiment analyzer
# vader_analyzer = SentimentIntensityAnalyzer()

def nlp_csv_to_video_pipeline(text):
    # Prepare input
    # model = AutoModelForSeq2SeqLM.from_pretrained('t5-base')
    # tokenizer = AutoTokenizer.from_pretrained('t5-base')
    input_text = f"summarize: {text}"
    inputs = summary_tokenizer.encode(input_text, return_tensors='pt', max_length=512, truncation=True)

    # Generate summary
    outputs = summary_model.generate(inputs, max_length=100)
    summary_text = summary_tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Extract percentages and categories using regex patterns
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

    # # Sentiment analysis
    # sentiment = vader_analyzer.polarity_scores(summary_text)
    # sentiment_label = 'positive' if sentiment['compound'] >= 0.05 else 'negative' if sentiment['compound'] <= -0.05 else 'neutral'

    # Text correction and language detection
    blob = TextBlob(summary_text)
    corrected_text = str(blob.correct())
    language = detect(corrected_text)  # Use langdetect to detect language

    # Generate audio
    tts = gTTS(corrected_text, lang='en')
    audio_filename = f'summary_audio_{uuid.uuid4().hex}.mp3'
    audio_path = os.path.join('D:\\1OOx-enginners-hackathon-submission-2\\media\\csv audio files', audio_filename)
    tts.save(audio_path)

    return {
        'categories': categories,
        'values': percentages,
        'text': corrected_text,
        'audio_path': audio_path,
        # 'sentiment': sentiment_label,
        'language': language
    }

# # Example usage
# if __name__ == "__main__":
#     text = "20% of users own an iPhone, 50% own a Samsung, and the rest own a variety of brands"
#     summary = nlp_pipeline(text)
#     print(summary)

def read_data(file_path):
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format")
    return df


def select_visualization_method(df):
    # Analyze the data and select appropriate visualization methods
    visualizations = []
    for column in df.columns:
        if df[column].dtype == 'object':
            visualizations.append(('bar', column))
        elif df[column].dtype in ['int64', 'float64']:
            if df[column].nunique() < 10:
                visualizations.append(('pie', column))
            else:
                visualizations.append(('line', column))
    return visualizations



def create_visualizations(df, visualizations, output_dir="D:\\1OOx-enginners-hackathon-submission-2\\media\\images"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    image_paths = []
    for viz_type, column in visualizations:
        fig, ax = plt.subplots(figsize=(10, 6))  # Ensure all images have the same size
        if viz_type == 'bar':
            df[column].value_counts().plot(kind='bar', ax=ax, color='skyblue')
            ax.set_title(f'{column} Distribution')
        elif viz_type == 'pie':
            df[column].value_counts().plot(kind='pie', ax=ax, autopct='%1.1f%%')
            ax.set_title(f'{column} Distribution')
        elif viz_type == 'line':
            df[column].plot(kind='line', ax=ax, color='skyblue')
            ax.set_title(f'{column} Trend')
        
        image_filename = f"{uuid.uuid4().hex}.png"
        image_path = os.path.join(output_dir, image_filename)
        plt.savefig(image_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        image_paths.append(image_path)
    
    return image_paths


def generate_video_from_images(image_paths, output_video_path, fps=10, max_resolution=(640, 480)):
    from moviepy.editor import ImageClip, concatenate_videoclips
    from PIL import Image
    import numpy as np
    import os
    import logging
    from tqdm import tqdm

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    # Resize images and store in memory
    resized_images = []
    for image_path in image_paths:
        try:
            image = Image.open(image_path).convert('RGB')
            resized_image = image.resize(max_resolution)
            resized_images.append(np.array(resized_image))
            logger.debug(f"Resized image: {image_path}")
        except Exception as e:
            logger.error(f"Error processing image {image_path}: {e}")
            continue

    # Process images in batches
    batch_size = 50
    batch_clips = []
    for i in range(0, len(resized_images), batch_size):
        batch = resized_images[i:i + batch_size]
        clips = [ImageClip(img).set_duration(5).fadein(1).fadeout(1) for img in batch]
        batch_clip = concatenate_videoclips(clips, method="compose")
        batch_clips.append(batch_clip)

    # Combine all batches
    final_clip = concatenate_videoclips(batch_clips, method="compose")
    final_clip.fps = fps

    # Write video to file with optimized settings
    output_video_path = os.path.abspath(output_video_path)
    try:
        final_clip.write_videofile(
            output_video_path,
            codec="libx264",
            preset="ultrafast",
            bitrate="500k"
        )
    except Exception as e:
        logger.error(f"Error writing video file: {e}")
        raise

    return output_video_path


def add_auto_generated_audio_to_video(video_path, audio_file_path, output_video_path):
    if video_path is None:
        logging.error("Video path is None, cannot add audio.")
        return None
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_file_path)

    # Set the audio of the video clip to the generated narration
    video_clip = video_clip.set_audio(audio_clip)

    # Write the final video with the audio
    video_clip.write_videofile(output_video_path, codec="libx264", audio_codec="aac")
    return output_video_path



def create_infographic_video(file_path):
    df = read_data(file_path)
    summary = nlp_csv_to_video_pipeline(df.to_string(index=False))
    visualizations = select_visualization_method(df)
    image_paths = create_visualizations(df, visualizations)
    video_path = generate_video_from_images(image_paths, f'video_{uuid.uuid4().hex}.mp4')
    if video_path is None:
        logging.error("Failed to generate video from images.")
        return
    final_video_path = add_auto_generated_audio_to_video(video_path, summary['audio_path'], f'final_video_{uuid.uuid4().hex}.mp4')
    if final_video_path is None:
        logging.error("Failed to add audio to video.")
        return
    print(f"Infographic video created successfully: {final_video_path}")
    
    
    return final_video_path
# def process_data_and_create_video(file_path):
#     # Create the infographic video
#     create_infographic_video(file_path)

# # Example usage
# if __name__ == "__main__":
#     file_path = 'D:\\1OOx-enginners-hackathon-submission-2\\data\\2015.csv'
#     process_data_and_create_video(file_path)