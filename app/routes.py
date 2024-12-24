
#----------------------------------------OLD CODE Pexels API Endpoints ---------------------------------------------------#

# from flask import Blueprint, render_template, request, jsonify
# # from .utils import parse_input_text, generate_video_from_text , nlp
# from .utils import nlp_pipeline , convert_gif_to_storytelling_video
# import logging
# # from video_preprocessing import convert_gif_to_storytelling_video 
# # from Preprocess_text_NLP import nlp_pipeline

# main = Blueprint('main', __name__)

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# @main.route("/")
# def index():
#     return render_template('index.html')

# @main.route("/text-to-video")
# def text_to_video():
#     return render_template('text-to-video.html')

# @main.route("/generate_video", methods=["POST"])
# def generate_video():
#     try:
#         input_text = request.json.get("text", "")
#         # data = parse_input_text(input_text)
#         parse_text = nlp_pipeline(input_text)
#         print("Parsed Data:", input_text)
#         if not input_text:
#             return jsonify({"error": "No text provided"}), 400

#         # Process input text and generate video URLs
#         video_urls = convert_gif_to_storytelling_video(parse_text)
#         logger.info(f"Generated video URLs for input: {input_text}")
#         return jsonify({"video_urls": video_urls})
#     except ValueError as ve:
#         logger.error(f"Invalid input: {str(ve)}")
#         return jsonify({"error": "Invalid input"}), 400
#     except Exception as e:
#         logger.error(f"An error occurred: {str(e)}")
#         return jsonify({"error": "An internal error occurred"}), 500



# ---------------------------OLD Endpoint not in use --------------------

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

#----------------------------------------OLD CODE---------------------------------------------------#



from flask import Blueprint, render_template, request, jsonify , send_file , send_from_directory
from .utils import nlp_pipeline, convert_gif_to_storytelling_video , create_animated_gif # Ensure correct import
import logging
import os
import time
# from  .text_processing import nlp_pipeline
# from  .gif_animation_creation import create_animated_gif
# from  .data_storytelling_video_processing import convert_gif_to_storytelling_video
from flask import Blueprint

# video_processing = Blueprint('video_processing', __name__)

main = Blueprint('main', __name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define path for static folder to serve video
UPLOADS_FOLDER = os.path.join(os.getcwd(), 'uploads', 'videos')
# Define the base path for uploads
UPLOADS_DIRECTORY = os.path.abspath("uploads/videos")



@main.route("/")
def index():
    return render_template('index.html')

@main.route("/text-to-video")
def text_to_video():
    return render_template('text-to-video.html')


@main.route('/uploads/videos/<filename>', methods=['GET'])
def serve_video(filename):
    # Serve the video file dynamically
    return send_from_directory(UPLOADS_DIRECTORY, filename, as_attachment=False)

@main.route("/generate_video", methods=["POST"])
def generate_video():
    try:
        input_text = request.json.get("text", "")
        if not input_text:
            return jsonify({"error": "Text is missing"}), 400

        # Create GIF and convert it to a video
        gif_path = create_animated_gif(input_text)
        video_path = convert_gif_to_storytelling_video(gif_path, input_text)

        # Ensure the uploads/videos directory exists
        os.makedirs(UPLOADS_FOLDER, exist_ok=True)

        # Save the generated video with a timestamped filename
        timestamp = int(time.time())
        video_filename = f"generated_video_{timestamp}.mp4"
        final_video_path = os.path.join(UPLOADS_FOLDER, video_filename)
        os.rename(video_path, final_video_path)

        logger.info(f"Generated video path: {final_video_path}")

        # Return the correct video path for the frontend
        return jsonify({"video_path": f"/uploads/videos/{video_filename}"}), 200

    except Exception as e:
        logger.error(f"Error generating video: {e}")
        return jsonify({"error": f"An internal error occurred: {str(e)}"}), 500

# working code 

