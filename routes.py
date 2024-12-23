# from flask import Blueprint, render_template, request, jsonify
# from  utils import parse_input_text, generate_video_from_text
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# main = Blueprint('main', __name__)

# @main.route("/")
# def index():
#     return render_template('index.html')

# @main.route("/generate_video", methods=["POST"])
# def generate_video():
#     try:
#         input_text = request.json.get("text", "")
#         if not input_text:
#             return jsonify({"error": "No text provided"}), 400

#         # Process the input and generate videos
#         parsed_data = parse_input_text(input_text)
#         logger.info(f"Parsed input: {parsed_data}")

#         video_urls = generate_video_from_text(parsed_data)
#         return jsonify({"video_urls": video_urls})
#     except ValueError as ve:
#         logger.error(f"Invalid input: {str(ve)}")
#         return jsonify({"error": "Invalid input"}), 400
#     except Exception as e:
#         logger.error(f"An error occurred: {str(e)}")
#         return jsonify({"error": "An internal error occurred"}), 500

# -------------------------------------OLD CODE-----------------------------------------------------------------------
# -------------------------------------OLD CODE-----------------------------------------------------------------------
# -------------------------------------OLD CODE-----------------------------------------------------------------------
# -------------------------------------OLD CODE-----------------------------------------------------------------------


from flask import Blueprint, render_template, request, jsonify
from utils import nlp_pipeline, convert_gif_to_storytelling_video
import logging
from flask import Flask, request, jsonify
import os
import pandas as pd
from gtts import gTTS
from transformers import pipeline
import matplotlib.pyplot as plt
from moviepy.editor import ImageSequenceClip



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return render_template('index.html')

@main.route("/generate_video", methods=["POST"])
def generate_video():
    try:
        input_text = request.json.get("text", "")
        if not input_text:
            return jsonify({"error": "No text provided"}), 400

        # Process the input and generate videos
        parsed_data = nlp_pipeline(input_text, '')
        logger.info(f"Parsed input: {parsed_data}")

        video_path = convert_gif_to_storytelling_video(parsed_data)
        return jsonify({"video_path": video_path})
    except ValueError as ve:
        logger.error(f"Invalid input: {str(ve)}")
        return jsonify({"error": "Invalid input"}), 400
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return jsonify({"error": "An internal error occurred"}), 500


# # Flask endpoint to handle text summarization and audio generation
# @app.route('/summarize', methods=['POST'])
# def summarize():
#     data = request.json
#     text = data.get('text', '')
#     if not text:
#         return jsonify({'error': 'No text provided'}), 400

#     summary, audio_path = summarize_and_generate_audio(text)
#     return jsonify({'summary': summary, 'audio_path': audio_path})

# # Flask endpoint to handle infographic generation
# @app.route('/infographics', methods=['POST'])
# def infographics():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file uploaded'}), 400

#     file = request.files['file']
#     csv_path = os.path.join("uploads", file.filename)
#     file.save(csv_path)

#     infographic_path = generate_infographics_from_csv(csv_path)
#     video_path = create_video_from_images([infographic_path])

#     return jsonify({'infographic_path': infographic_path, 'video_path': video_path})

# if __name__ == '__main__':
#     os.makedirs("uploads", exist_ok=True)
#     app.run(debug=True)
