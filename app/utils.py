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
    tts.save('F:\\100x_enginners_hackathon_genai\\uploads\\audio_files\\summary_audio.mp3')
    
    return {
        'categories': categories,
        'values': percentages,
        'text': summary_text
    }


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
    
    
    
    
    
def create_animated_gif(text):
    import os
    from PIL import Image
    import matplotlib.pyplot as plt
    
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
    
    gif_path = 'F:\\100x_enginners_hackathon_genai\\generated_images\\animated_infographic.gif'
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



def create_animated_gif(text):
    import os
    from PIL import Image
    import matplotlib.pyplot as plt
    import shutil  # For directory removal
    
    # Use the NLP pipeline to process the text
    summary = nlp_pipeline(text, '')
    categories = summary['categories']
    values = summary['values']
    
    # Create frames directory
    frames_dir = 'animation_frames'
    if os.path.exists(frames_dir):
        shutil.rmtree(frames_dir)  # Remove directory if it exists
    os.makedirs(frames_dir)
    
    def create_frame(frame_number, value_multiplier, categories=categories, values=values):
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
    
    gif_path = 'F:\\100x_enginners_hackathon_genai\\generated_images\\animated_infographic.gif'
    images[0].save(
        gif_path,
        save_all=True,
        append_images=images[1:],
        duration=100,  # 100ms between frames
        loop=0
    )
    
    # Clean up frames directory
    try:
        shutil.rmtree(frames_dir)
        print("Cleanup completed successfully")
    except Exception as e:
        print(f"Cleanup error: {e}")
    
    print(f"Animation saved as GIF: {gif_path}")
    return gif_path





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




# # Create the animated GIF
# gif_path = create_animated_gif('30% dogs use nokia and 90% use iphones')

# # Convert to storytelling video
# video_path = convert_gif_to_storytelling_video(gif_path, '30% dogs use nokia and 90% use iphones')




# --------------------------------------OLD Code Pexels API Implementation  --------------------------------



# # Load environment variables
# load_dotenv()


# PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
# print(f"Your API Key: {PEXELS_API_KEY}")

# # Text processing functions
# def parse_input_text(text):
#     data_points = {}
#     parts = text.split(',')
#     for part in parts:
#         part = part.strip()
#         if '%' in part:
#             key, value = part.split('%')
#             data_points[key.strip()] = float(value.strip().replace('%', '')) / 100
#         else:
#             try:
#                 key_value = part.split(' ', 1)
#                 if len(key_value) == 2:
#                     key, value = key_value
#                     data_points[key.strip()] = value.strip()
#                 else:
#                     try:
#                         data_points[part] = float(part)
#                     except ValueError:
#                         print(f"Could not parse part: '{part}'")
#             except ValueError:
#                 print(f"Could not parse part: '{part}'")
#                 continue

#     # Additional processing to convert data points into relevant information
#     relevant_info = {}
#     for key, value in data_points.items():
#         if isinstance(value, float):
#             relevant_info[key] = f"{value * 100}%"
#         else:
#             relevant_info[key] = value

#     return relevant_info


# def preprocess_text(text):
#     cleaned_text = text.strip().lower()
#     cleaned_text = ' '.join(sorted(set(cleaned_text.split()), key=lambda x: cleaned_text.index(x)))
#     return cleaned_text


# def analyze_sentiment(text):
#     analysis = TextBlob(text)
#     return analysis.sentiment.polarity


# def semantic_segment_transformation(text):
#     contextual_prompt = f"Contextual prompt based on: {text}"
#     return contextual_prompt



# # Video Generation Function
# def generate_video_from_text(text):
#     # data = parse_input_text(text)
#     print("Parsed Data:", text)
    
#     contextual_prompt = semantic_segment_transformation(text)
#     processed_prompt = preprocess_text(contextual_prompt)
#     visualization_prompt = f"Create an animated infographic video showing the distribution of: {processed_prompt}"

#     headers = {'Authorization': PEXELS_API_KEY}
#     params = {'query': f'infographics {visualization_prompt}', 'per_page': 5}

#     time.sleep(3)
#     response = requests.get('https://api.pexels.com/videos/search', headers=headers, params=params)
    
#     if response.status_code != 200:
#         raise Exception(f"Pexels API request failed with status code {response.status_code}")

#     videos = response.json().get('videos', [])
#     video_urls = [video['video_files'][0]['link'] for video in videos if video['video_files']]
    
#     time.sleep(3)
#     return video_urls[:3]


# # Log types
# LOG_TYPE_GPT = "GPT"
# LOG_TYPE_PEXEL = "PEXEL"

# # log directory paths
# DIRECTORY_LOG_GPT = ".logs/gpt_logs"
# DIRECTORY_LOG_PEXEL = ".logs/pexel_logs"

# # method to log response from pexel and openai
# def log_response(log_type, query,response):
#     log_entry = {
#         "query": query,
#         "response": response,
#         "timestamp": datetime.now().isoformat()
#     }
#     if log_type == LOG_TYPE_GPT:
#         if not os.path.exists(DIRECTORY_LOG_GPT):
#             os.makedirs(DIRECTORY_LOG_GPT)
#         filename = '{}_gpt3.txt'.format(datetime.now().strftime("%Y%m%d_%H%M%S"))
#         filepath = os.path.join(DIRECTORY_LOG_GPT, filename)
#         with open(filepath, "w") as outfile:
#             outfile.write(json.dumps(log_entry) + '\n')

#     if log_type == LOG_TYPE_PEXEL:
#         if not os.path.exists(DIRECTORY_LOG_PEXEL):
#             os.makedirs(DIRECTORY_LOG_PEXEL)
#         filename = '{}_pexel.txt'.format(datetime.now().strftime("%Y%m%d_%H%M%S"))
#         filepath = os.path.join(DIRECTORY_LOG_PEXEL, filename)
#         with open(filepath, "w") as outfile:
#             outfile.write(json.dumps(log_entry) + '\n')



# --------------------------------------OLD Code Pexels API Implementation  --------------------------------