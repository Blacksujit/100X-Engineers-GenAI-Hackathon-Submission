from flask import Blueprint, render_template, request, jsonify
from .utils import parse_input_text, generate_video_from_text
import logging

main = Blueprint('main', __name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@main.route("/")
def index():
    return render_template('index.html')

@main.route("/text-to-video")
def text_to_video():
    return render_template('text-to-video.html')

@main.route("/generate_video", methods=["POST"])
def generate_video():
    try:
        input_text = request.json.get("text", "")
        data = parse_input_text(input_text)
        print("Parsed Data:", data)
        if not data:
            return jsonify({"error": "No text provided"}), 400

        # Process input text and generate video URLs
        video_urls = generate_video_from_text(data)
        logger.info(f"Generated video URLs for input: {input_text}")
        return jsonify({"video_urls": video_urls})
    except ValueError as ve:
        logger.error(f"Invalid input: {str(ve)}")
        return jsonify({"error": "Invalid input"}), 400
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return jsonify({"error": "An internal error occurred"}), 500
