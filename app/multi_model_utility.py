import pandas as pd
import logging
from sklearn.preprocessing import StandardScaler
from transformers import BartTokenizer, BartForConditionalGeneration
import logging
import re
import spacy
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from PIL import Image
import random
from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_videoclips
import os
import time
import torch
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import os
from PIL import Image
from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip, TextClip
import numpy as np
import io
import pandas as pd
import time
from matplotlib.animation import FuncAnimation
from gtts import gTTS
from transformers import BartTokenizer, BartForConditionalGeneration
import spacy
import re
import pandas as pd
import logging
from sklearn.preprocessing import StandardScaler
import pandas as pd
import logging
from sklearn.preprocessing import StandardScaler
import pandas as pd
import logging
from sklearn.preprocessing import StandardScaler
import pickle
from transformers import BartTokenizer, BartForConditionalGeneration
import spacy
import os
import logging
import warnings 
import logging
import io
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from matplotlib.animation import FuncAnimation
import imageio
import re
import logging
from transformers import BartTokenizer, BartForConditionalGeneration
import joblib
import os

# nlp = spacy.load("en_core_web_sm")

# Setting up logging
logging.basicConfig(level=logging.INFO)

# # Load spaCy model for NER
# nlp = spacy.load("en_core_web_sm")

os.environ['HF_HOME'] = "D:\\cahc_models_folder"  # Change this to your desired cache path


def load_models(model_directory="models"):
    # Load the tokenizer and model from the saved .pkl files
    with open(os.path.join(model_directory, "facebook_tokenizer_joblib.pkl"), "rb") as f:
        tokenizer = joblib.load(f)
    with open(os.path.join(model_directory, "facebook_model_joblib.pkl"), "rb") as f:
        model = joblib.load(f)
    
    # Load the spaCy model from the saved .pkl file
    with open(os.path.join(model_directory, "spacy_model_joblib.pkl"), "rb") as f:
        nlp = joblib.load(f)
    
    return tokenizer, model, nlp

# Load the models
tokenizer, model, nlp = load_models()


def load_and_preprocess_data(file_path):
    try:
        logging.info(f"Loading data from {file_path}")
        # Load data
        if file_path.endswith('.csv'):
            data = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            data = pd.read_excel(file_path)
        elif file_path.endswith('.txt'):
            data = pd.read_csv(file_path, delimiter='\t')
        else:
            raise ValueError("Unsupported file format.")
        
        logging.info("Data loaded successfully")
        
        # Detect and convert data types
        for col in data.columns:
            try:
                data[col] = pd.to_numeric(data[col], errors='coerce')
            except ValueError:
                pass
        
        # Handle missing values
        data.fillna(data.mean(), inplace=True)
        
        # Handle categorical data
        categorical_cols = data.select_dtypes(include=['object']).columns
        data = pd.get_dummies(data, columns=categorical_cols, drop_first=True)
        
        # Normalize numeric data
        numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
        scaler = StandardScaler()
        data[numeric_cols] = scaler.fit_transform(data[numeric_cols])
        
        logging.info("Data preprocessing completed")
        return data
    except Exception as e:
        logging.error(f"Error loading and preprocessing data: {e}")
        raise
    
    
import logging
import pandas as pd

def perform_eda(data):
    try:
        logging.info("Performing EDA...")
        
        # Basic EDA summary
        eda_summary = {
            "shape": data.shape,
            "columns": data.columns.tolist(),
            "dtypes": data.dtypes.apply(lambda x: x.name).to_dict(),
            "null_counts": data.isnull().sum().to_dict(),
            "describe": data.describe(include='all').to_dict()
        }
        
        # Correlation analysis
        numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
        if len(numeric_cols) > 1:
            eda_summary["correlation"] = data[numeric_cols].corr().to_dict()
        
        # Unique value counts
        eda_summary["unique_counts"] = {col: data[col].nunique() for col in data.columns}
        
        # Missing value analysis
        eda_summary["missing_value_analysis"] = {
            "total_missing": data.isnull().sum().sum(),
            "missing_per_column": data.isnull().sum().to_dict(),
            "missing_percentage_per_column": (data.isnull().sum() / len(data) * 100).to_dict()
        }
        
        # Categorical data analysis
        categorical_cols = data.select_dtypes(include=['object']).columns
        eda_summary["categorical_summary"] = {
            col: data[col].value_counts().to_dict() for col in categorical_cols
        }
        
        # Outlier detection
        eda_summary["outliers"] = {
            col: data[col][((data[col] - data[col].mean()) / data[col].std()).abs() > 3].tolist() for col in numeric_cols
        }
        
        # Distribution analysis
        eda_summary["distribution"] = {
            col: data[col].describe().to_dict() for col in numeric_cols
        }
        
        # Time series analysis
        date_cols = [col for col in data.columns if 'date' in col.lower() or 'time' in col.lower()]
        if date_cols:
            eda_summary["time_series_analysis"] = {
                col: data.set_index(col).resample('M').mean().to_dict() for col in date_cols if pd.api.types.is_datetime64_any_dtype(data[col])
            }
        
        logging.debug(f"EDA Summary: {eda_summary}")
        return eda_summary
    except Exception as e:
        logging.error(f"Error performing EDA: {e}")
        raise
    
    


def analyze_prompt_for_insights(prompt, eda_summary):
    try:
        logging.info("Analyzing prompt for insights")
        
        inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
        input_ids = inputs.input_ids
        attention_mask = inputs.attention_mask
        
        outputs = model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_length=200,
            num_return_sequences=1,
            temperature=0.7,
            top_p=0.9,
            top_k=50,
            no_repeat_ngram_size=2,
            pad_token_id=tokenizer.eos_token_id
        )
        
        generated_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
        logging.debug(f"Generated text from model: {generated_text}")
        
        insights, columns = extract_insights_and_columns_from_text(generated_text, eda_summary)
        
        if not insights:
            logging.warning("No insights could be extracted from the provided prompt. Using fallback insights.")
            insights = fallback_insights(eda_summary)
        
        if not columns:
            logging.warning("No columns could be extracted from the provided prompt. Using fallback columns.")
            columns = fallback_columns(eda_summary)
        
        logging.info(f"Insights extracted: {insights}")
        logging.info(f"Columns extracted: {columns}")
        return insights, columns
    except Exception as e:
        logging.error(f"Error in analyzing prompt for insights: {e}")
        return [], []

def extract_insights_and_columns_from_text(text, eda_summary):
    possible_insights = ["trend", "comparison", "distribution", "correlation", "pattern", "anomaly", "outlier", "relationship", "performance", "growth"]
    insights = []
    columns = []
    
    text = text.lower()
    
    for insight in possible_insights:
        if re.search(r'\b' + re.escape(insight) + r'\b', text):
            insights.append(insight)
    
    # Extract column names from the text
    # Assuming column names are mentioned in the text and are separated by commas
    column_pattern = re.compile(r'\b(?:columns|fields|attributes|features)\b\s*:\s*([\w\s,]+)')
    match = column_pattern.search(text)
    if match:
        columns = [col.strip() for col in match.group(1).split(',')]
    
    # Validate columns against EDA summary
    valid_columns = [col for col in columns if col in eda_summary['columns']]
    
    return insights, valid_columns

def fallback_insights(eda_summary):
    # Fallback logic to generate default insights based on EDA summary
    insights = []
    if len(eda_summary['columns']) > 1:
        insights.append("correlation")
    if any('date' in col.lower() or 'time' in col.lower() for col in eda_summary['columns']):
        insights.append("trend")
    if any(eda_summary['dtypes'][col] == 'object' for col in eda_summary['columns']):
        insights.append("distribution")
    return insights

def fallback_columns(eda_summary):
    # Fallback logic to generate default columns based on EDA summary
    numeric_columns = [col for col in eda_summary['columns'] if eda_summary['dtypes'][col] in ['float64', 'int64']]
    if len(numeric_columns) >= 2:
        return numeric_columns[:2]
    return numeric_columns



def generate_animated_frames(data, insights, columns, output_dir="frames"):
    logging.info("Generating animated frames from data")
    frames = []
    
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Log the data columns and types
    logging.debug(f"Data columns: {data.columns}")
    logging.debug(f"Data types: {data.dtypes}")
    
    # Generate frames based on insights
    for insight in insights:
        logging.debug(f"Processing insight: {insight}")
        if insight == "trend":
            logging.info("Generating trend frames")
            date_column = None
            for col in data.columns:
                if 'date' in col.lower() or 'time' in col.lower():
                    date_column = col
                    break
            
            if date_column and columns:
                numeric_columns = [col for col in columns if col in data.columns and data[col].dtype in ['float64', 'int64']]
                if len(numeric_columns) > 0:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    lines = [ax.plot([], [], label=col)[0] for col in numeric_columns]
                    ax.set_xlim(data[date_column].min(), data[date_column].max())
                    ax.set_ylim(data[numeric_columns].min().min(), data[numeric_columns].max().max())
                    ax.set_title(f"Time Series Plot for {', '.join(numeric_columns)}")
                    ax.set_xlabel('Time')
                    ax.set_ylabel('Values')
                    ax.legend()

                    def update(frame):
                        for line, col in zip(lines, numeric_columns):
                            line.set_data(data[date_column][:frame], data[col][:frame])
                        return lines

                    ani = FuncAnimation(fig, update, frames=len(data), blit=True)
                    for i in range(len(data)):
                        update(i)
                        buf = io.BytesIO()
                        fig.savefig(buf, format='png')
                        buf.seek(0)
                        img = Image.open(buf)
                        frames.append(np.array(img))
                    plt.close(fig)
                else:
                    logging.warning("No numeric columns found for trend insight")
            else:
                logging.warning("No date column or relevant columns found for trend insight")
        
        elif insight == "comparison":
            logging.info("Generating comparison frames")
            if len(columns) == 2 and all(col in data.columns for col in columns):
                fig, ax = plt.subplots(figsize=(10, 6))
                categories = data[columns[0]].unique()
                bars = ax.bar(categories, np.zeros(len(categories)))
                ax.set_ylim(0, data[columns[1]].max())
                ax.set_title('Animated Bar Chart')
                ax.set_xlabel(columns[0])
                ax.set_ylabel(columns[1])

                def update_bar(frame):
                    for bar, category in zip(bars, categories):
                        bar.set_height(data[data[columns[0]] == category][columns[1]].iloc[frame])
                    return bars

                ani = FuncAnimation(fig, update_bar, frames=len(data), blit=True)
                for i in range(len(data)):
                    update_bar(i)
                    buf = io.BytesIO()
                    fig.savefig(buf, format='png')
                    buf.seek(0)
                    img = Image.open(buf)
                    frames.append(np.array(img))
                plt.close(fig)
            else:
                logging.warning("Required columns for comparison insight not found or incorrect")
        
        elif insight == "distribution":
            logging.info("Generating distribution frames")
            numeric_columns = [col for col in columns if col in data.columns and data[col].dtype in ['float64', 'int64']]
            if len(numeric_columns) > 0:
                for col in numeric_columns:
                    fig, ax = plt.subplots(figsize=(8, 6))
                    sns.histplot(data[col], bins=10, kde=True, ax=ax)
                    ax.set_title(f"Distribution of {col}")
                    buf = io.BytesIO()
                    fig.savefig(buf, format='png')
                    buf.seek(0)
                    img = Image.open(buf)
                    frames.append(np.array(img))
                    plt.close(fig)
            else:
                logging.warning("No numeric columns found for distribution insight")
        
        elif insight == "correlation":
            logging.info("Generating correlation frames")
            numeric_columns = [col for col in columns if col in data.columns and data[col].dtype in ['float64', 'int64']]
            if len(numeric_columns) > 1:
                corr_matrix = data[numeric_columns].corr()
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, ax=ax)
                ax.set_title('Correlation Matrix')
                buf = io.BytesIO()
                fig.savefig(buf, format='png')
                buf.seek(0)
                img = Image.open(buf)
                frames.append(np.array(img))
                plt.close(fig)
            else:
                logging.warning("Not enough numeric columns for correlation insight")
        
        elif insight == "pie":
            logging.info("Generating pie chart frames")
            if len(columns) == 2 and all(col in data.columns for col in columns):
                fig, ax = plt.subplots(figsize=(10, 6))
                def update_pie(frame):
                    ax.clear()
                    ax.pie(data[columns[1]][:frame], labels=data[columns[0]][:frame], autopct='%1.1f%%')
                    ax.set_title('Animated Pie Chart')

                ani = FuncAnimation(fig, update_pie, frames=len(data), blit=True)
                for i in range(len(data)):
                    update_pie(i)
                    buf = io.BytesIO()
                    fig.savefig(buf, format='png')
                    buf.seek(0)
                    img = Image.open(buf)
                    frames.append(np.array(img))
                plt.close(fig)
            else:
                logging.warning("Required columns for pie chart insight not found or incorrect")
        
        elif insight == "pattern":
            logging.info("Generating pattern frames")
            # Example: Detecting and animating a repeating pattern in a time series
            date_column = None
            for col in data.columns:
                if 'date' in col.lower() or 'time' in col.lower():
                    date_column = col
                    break
            
            if date_column and columns:
                numeric_columns = [col for col in columns if col in data.columns and data[col].dtype in ['float64', 'int64']]
                if len(numeric_columns) > 0:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    lines = [ax.plot([], [], label=col)[0] for col in numeric_columns]
                    ax.set_xlim(data[date_column].min(), data[date_column].max())
                    ax.set_ylim(data[numeric_columns].min().min(), data[numeric_columns].max().max())
                    ax.set_title(f"Pattern Detection for {', '.join(numeric_columns)}")
                    ax.set_xlabel('Time')
                    ax.set_ylabel('Values')
                    ax.legend()

                    def update(frame):
                        for line, col in zip(lines, numeric_columns):
                            line.set_data(data[date_column][:frame], data[col][:frame])
                        return lines

                    ani = FuncAnimation(fig, update, frames=len(data), blit=True)
                    for i in range(len(data)):
                        update(i)
                        buf = io.BytesIO()
                        fig.savefig(buf, format='png')
                        buf.seek(0)
                        img = Image.open(buf)
                        frames.append(np.array(img))
                    plt.close(fig)
                else:
                    logging.warning("No numeric columns found for pattern insight")
            else:
                logging.warning("No date column or relevant columns found for pattern insight")

        elif insight == "anomaly":
            logging.info("Generating anomaly frames")
            # Example: Highlighting anomalies in a time series
            date_column = None
            for col in data.columns:
                if 'date' in col.lower() or 'time' in col.lower():
                    date_column = col
                    break
            
            if date_column and columns:
                numeric_columns = [col for col in columns if col in data.columns and data[col].dtype in ['float64', 'int64']]
                if len(numeric_columns) > 0:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    lines = [ax.plot([], [], label=col)[0] for col in numeric_columns]
                    ax.set_xlim(data[date_column].min(), data[date_column].max())
                    ax.set_ylim(data[numeric_columns].min().min(), data[numeric_columns].max().max())
                    ax.set_title(f"Anomaly Detection for {', '.join(numeric_columns)}")
                    ax.set_xlabel('Time')
                    ax.set_ylabel('Values')
                    ax.legend()

                    def update(frame):
                        for line, col in zip(lines, numeric_columns):
                            line.set_data(data[date_column][:frame], data[col][:frame])
                            if data[col][frame] > data[col].mean() + 3 * data[col].std() or data[col][frame] < data[col].mean() - 3 * data[col].std():
                                line.set_color('red')
                            else:
                                line.set_color('blue')
                        return lines

                    ani = FuncAnimation(fig, update, frames=len(data), blit=True)
                    for i in range(len(data)):
                        update(i)
                        buf = io.BytesIO()
                        fig.savefig(buf, format='png')
                        buf.seek(0)
                        img = Image.open(buf)
                        frames.append(np.array(img))
                    plt.close(fig)
                else:
                    logging.warning("No numeric columns found for anomaly insight")
            else:
                logging.warning("No date column or relevant columns found for anomaly insight")

        elif insight == "outlier":
            logging.info("Generating outlier frames")
            # Example: Highlighting outliers in a scatter plot
            if len(columns) == 2 and all(col in data.columns for col in columns):
                fig, ax = plt.subplots(figsize=(10, 6))
                scatter = ax.scatter(data[columns[0]], data[columns[1]], c='blue')
                ax.set_title('Outlier Detection')
                ax.set_xlabel(columns[0])
                ax.set_ylabel(columns[1])

                def update(frame):
                    ax.clear()
                    ax.scatter(data[columns[0]], data[columns[1]], c='blue')
                    outliers = data[(data[columns[1]] > data[columns[1]].mean() + 3 * data[columns[1]].std()) | (data[columns[1]] < data[columns[1]].mean() - 3 * data[columns[1]].std())]
                    ax.scatter(outliers[columns[0]], outliers[columns[1]], c='red')
                    ax.set_title('Outlier Detection')
                    ax.set_xlabel(columns[0])
                    ax.set_ylabel(columns[1])
                    return scatter,

                ani = FuncAnimation(fig, update, frames=len(data), blit=True)
                for i in range(len(data)):
                    update(i)
                    buf = io.BytesIO()
                    fig.savefig(buf, format='png')
                    buf.seek(0)
                    img = Image.open(buf)
                    frames.append(np.array(img))
                plt.close(fig)
            else:
                logging.warning("Required columns for outlier insight not found or incorrect")

        elif insight == "relationship":
            logging.info("Generating relationship frames")
            # Example: Showing relationship between two variables over time
            if len(columns) == 2 and all(col in data.columns for col in columns):
                fig, ax = plt.subplots(figsize=(10, 6))
                scatter = ax.scatter(data[columns[0]], data[columns[1]], c='blue')
                ax.set_title('Relationship Over Time')
                ax.set_xlabel(columns[0])
                ax.set_ylabel(columns[1])

                def update(frame):
                    ax.clear()
                    ax.scatter(data[columns[0]][:frame], data[columns[1]][:frame], c='blue')
                    ax.set_title('Relationship Over Time')
                    ax.set_xlabel(columns[0])
                    ax.set_ylabel(columns[1])
                    return scatter,

                ani = FuncAnimation(fig, update, frames=len(data), blit=True)
                for i in range(len(data)):
                    update(i)
                    buf = io.BytesIO()
                    fig.savefig(buf, format='png')
                    buf.seek(0)
                    img = Image.open(buf)
                    frames.append(np.array(img))
                plt.close(fig)
            else:
                logging.warning("Required columns for relationship insight not found or incorrect")

        elif insight == "performance":
            logging.info("Generating performance frames")
            # Example: Showing performance metrics over time
            date_column = None
            for col in data.columns:
                if 'date' in col.lower() or 'time' in col.lower():
                    date_column = col
                    break
            
            if date_column and columns:
                numeric_columns = [col for col in columns if col in data.columns and data[col].dtype in ['float64', 'int64']]
                if len(numeric_columns) > 0:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    lines = [ax.plot([], [], label=col)[0] for col in numeric_columns]
                    ax.set_xlim(data[date_column].min(), data[date_column].max())
                    ax.set_ylim(data[numeric_columns].min().min(), data[numeric_columns].max().max())
                    ax.set_title(f"Performance Metrics for {', '.join(numeric_columns)}")
                    ax.set_xlabel('Time')
                    ax.set_ylabel('Values')
                    ax.legend()

                    def update(frame):
                        for line, col in zip(lines, numeric_columns):
                            line.set_data(data[date_column][:frame], data[col][:frame])
                        return lines

                    ani = FuncAnimation(fig, update, frames=len(data), blit=True)
                    for i in range(len(data)):
                        update(i)
                        buf = io.BytesIO()
                        fig.savefig(buf, format='png')
                        buf.seek(0)
                        img = Image.open(buf)
                        frames.append(np.array(img))
                    plt.close(fig)
                else:
                    logging.warning("No numeric columns found for performance insight")
            else:
                logging.warning("No date column or relevant columns found for performance insight")

        elif insight == "growth":
            logging.info("Generating growth frames")
            # Example: Showing growth over time
            date_column = None
            for col in data.columns:
                if 'date' in col.lower() or 'time' in col.lower():
                    date_column = col
                    break
            
            if date_column and columns:
                numeric_columns = [col for col in columns if col in data.columns and data[col].dtype in ['float64', 'int64']]
                if len(numeric_columns) > 0:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    lines = [ax.plot([], [], label=col)[0] for col in numeric_columns]
                    ax.set_xlim(data[date_column].min(), data[date_column].max())
                    ax.set_ylim(data[numeric_columns].min().min(), data[numeric_columns].max().max())
                    ax.set_title(f"Growth Over Time for {', '.join(numeric_columns)}")
                    ax.set_xlabel('Time')
                    ax.set_ylabel('Values')
                    ax.legend()

                    def update(frame):
                        for line, col in zip(lines, numeric_columns):
                            line.set_data(data[date_column][:frame], data[col][:frame])
                        return lines

                    ani = FuncAnimation(fig, update, frames=len(data), blit=True)
                    for i in range(len(data)):
                        update(i)
                        buf = io.BytesIO()
                        fig.savefig(buf, format='png')
                        buf.seek(0)
                        img = Image.open(buf)
                        frames.append(np.array(img))
                    plt.close(fig)
                else:
                    logging.warning("No numeric columns found for growth insight")
            else:
                logging.warning("No date column or relevant columns found for growth insight")
        
        else:
            logging.warning(f"Unhandled insight type: {insight}")
    
    logging.info(f"Generated {len(frames)} animated frames")
    
    return frames




def create_video_from_frames(frames, audio_file=None, video_file="final_production_model.mp4"):
    if not frames:
        raise ValueError("No frames to create video from.")
    
    logging.info("Creating video from frames")
    video_clips = []
    for frame in frames:
        img_clip = ImageSequenceClip([frame], fps=1)  # 1 frame per second
        img_clip = img_clip.set_duration(2)  # Each frame lasts 2 seconds
        video_clips.append(img_clip)
    
    video = concatenate_videoclips(video_clips, method="compose")
    
    if audio_file and os.path.isfile(audio_file):
        audio = AudioFileClip(audio_file)
        video = video.set_audio(audio)
    
    video.write_videofile(video_file, codec="libx264", fps=24)
    logging.info(f"Video saved as {video_file}")

def generate_infographic_video(data, insights, columns,audio_file=None, title_image="title_screen.png"):
    frames = generate_animated_frames(data, insights, columns)
    if not frames:
        raise ValueError("No frames generated from data.")
    
    if os.path.exists(title_image):
        title_image_clip = Image.open(title_image)
        title_image_clip = title_image_clip.convert("RGBA")
        title_image_clip = np.array(title_image_clip)
        frames.insert(0, title_image_clip)
    
    create_video_from_frames(frames, audio_file)
    print("Video successfully generated!")
    
    
    
def generate_narration(text, output_file="narration.mp3", lang='en', slow=False, tld='com'):
    """
    Generate narration audio from text using gTTS (Google Text-to-Speech).

    Parameters:
    text (str): The text to be converted to speech.
    output_file (str): The file path where the audio file will be saved.
    lang (str): The language in which the text will be spoken. Default is 'en' (English).
    slow (bool): Whether to speak slowly. Default is False.
    tld (str): Top-level domain for the Google Translate host. Default is 'com'.

    Returns:
    str: The file path of the saved audio file.
    """
    try:
        logging.info(f"Generating narration for text: {text}")
        tts = gTTS(text=text, lang=lang, slow=slow, tld=tld)
        tts.save(output_file)
        logging.info(f"Narration saved to {output_file}")
        return output_file
    except Exception as e:
        logging.error(f"Error generating narration: {e}")
        raise

    
def data_storytelling_pipeline(file_path, prompt):
    try:
        start_time = time.time()
        
        logging.info("Loading and preprocessing data...")
        data = load_and_preprocess_data(file_path)
        logging.debug(f"Loaded Data: {data.head()}")
        
        logging.info("Performing EDA...")
        eda_summary = perform_eda(data)
        logging.debug(f"EDA Summary: {eda_summary}")
        
        logging.info("Analyzing the user's prompt...")
        insights, columns = analyze_prompt_for_insights(prompt, eda_summary)
        logging.debug(f"Extracted insights: {insights}")
        logging.debug(f"Extracted columns: {columns}")
        
        logging.info("Generating narration...")
        narration_text = f"Here is the analysis based on the prompt: {prompt}. Insights: {', '.join(insights)}"
        narration_file = generate_narration(narration_text)
        
        logging.info("Creating the infographic video...")
        # video_file = "final_production_model.mp4"
        generate_infographic_video(data, insights, columns, audio_file=narration_file)
        
        end_time = time.time()
        logging.info(f"Pipeline completed successfully in {end_time - start_time:.2f} seconds")
        
        # return video_file
    
    except FileNotFoundError as fnf_error:
        logging.error(f"File not found: {fnf_error}")
        raise
    except pd.errors.ParserError as parser_error:
        logging.error(f"Error parsing the file: {parser_error}")
        raise
    except TypeError as type_error:
        logging.error(f"Type error: {type_error}")
        raise
    except ValueError as value_error:
        logging.error(f"Value error: {value_error}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise    
  
# now used in project for user input uncomment only for model developement======================================================================  
  
# # Example usage:
# file_path = 'D:\\1OOx-enginners-hackathon-submission-2\\data\\main_data.csv'
# prompt = "number of accomodations average what would be in cool video"
# audio_file = "D:\\1OOx-enginners-hackathon-submission-2\\uploads\\audio_files"
# title_image = "D:\\1OOx-enginners-hackathon-submission-2\\outputs"

# if not os.path.exists(file_path):
#     raise FileNotFoundError(f"Data file not found: {file_path}")
# if not os.path.exists(audio_file):
#     raise FileNotFoundError(f"Audio file not found: {audio_file}")
# if not os.path.exists(title_image):
#     raise FileNotFoundError(f"Title image not found: {title_image}")

# data_storytelling_pipeline(file_path, prompt)


# now used in project for user input uncomment only for model developement======================================================================  


