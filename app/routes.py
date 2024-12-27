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
import shutil
import time
from .second_utility import create_scenario_based_infographic_video , create_animated_pie_chart , parse_user_input , generate_audio_from_text, generate_narration, add_auto_generated_audio_to_video
# from  .text_processing import nlp_pipeline
# from  .gif_animation_creation import create_animated_gif
# from  .data_storytelling_video_processing import convert_gif_to_storytelling_video
# from flask import Blueprint
from werkzeug.utils import secure_filename
import os
# video_processing = Blueprint('video_processing', __name__)

main = Blueprint('main', __name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define path for static folder to serve video
UPLOADS_FOLDER = os.path.join(os.getcwd(), 'uploads', 'videos')
# Define the base path for uploads
UPLOADS_DIRECTORY = os.path.abspath("uploads/videos")

UPLOADS_FOLDER = 'D:\\1OOx-enginners-hackathon-submission-2\\uploads\\videos'

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}  # add more if needed

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route("/")
def index():
    return render_template('index.html')

@main.route("/text-to-video")
def text_to_video():
    return render_template('text-to-video.html')

@main.route('/uploads/videos/<filename>',methods=['GET'])
def uploaded_file(filename):
    return send_from_directory(UPLOADS_FOLDER, filename)

# Old Route IN USEE ---------------------------------------------------------------
@main.route("/generate_video", methods=["POST"])
def generate_video():
    try:
        # Step 1: Extract input text
        input_text = request.json.get("text", "")
        if not input_text or not isinstance(input_text, str):
            return jsonify({"error": "Invalid or missing text input"}), 400

        logger.debug(f"Input text received: {input_text}")

        # Step 2: Parse input text using the ML pipeline
        try:
            parsed_data = nlp_pipeline(input_text, "")  # Your ML model processes the text
            logger.debug(f"Parsed data: {parsed_data}")
        except Exception as e:
            logger.error(f"Error in NLP pipeline: {e}")
            return jsonify({"error": "Failed to process text input"}), 500

        # Ensure parsed_data has the required structure
        if not isinstance(parsed_data, dict) or not all(key in parsed_data for key in ["categories", "values", "text"]):
            logger.error(f"Unexpected parsed_data format: {parsed_data}")
            return jsonify({"error": "Internal processing error"}), 500

        # Step 3: Generate an animated GIF using the parsed data
        try:
            gif_path = create_animated_gif(input_text)  # Use your existing function
            logger.debug(f"Generated GIF path: {gif_path}")
        except Exception as e:
            logger.error(f"Error generating GIF: {e}")
            return jsonify({"error": "Failed to generate GIF"}), 500

        # Step 4: Convert the GIF to a video
        try:
            video_path = convert_gif_to_storytelling_video(gif_path, input_text)  # Use your existing function
            logger.debug(f"Generated video path: {video_path}")
        except Exception as e:
            logger.error(f"Error converting GIF to video: {e}")
            return jsonify({"error": "Failed to convert GIF to video"}), 500

        # Step 5: Save the video and respond with the file path
        os.makedirs(UPLOADS_FOLDER, exist_ok=True)
        timestamp = int(time.time())
        video_filename = f"generated_video_{timestamp}.mp4"
        final_video_path = os.path.join(UPLOADS_FOLDER, video_filename)

        # Ensure the final video path is unique
        counter = 1
        while os.path.exists(final_video_path):
            video_filename = f"generated_video_{timestamp}_{counter}.mp4"
            final_video_path = os.path.join(UPLOADS_FOLDER, video_filename)
            counter += 1

        shutil.move(video_path, final_video_path)
        print('the video path is saved as:', final_video_path)

        return jsonify({"video_path": f"/uploads/videos/{video_filename}"}), 200

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

# working code 

# Old Route IN USEE ---------------------------------------------------------------

# Second Test Pass --- Working code routes 

# ------------------------------------backup route if the code gets lost ------------------------------

# @main.route("/generate_video", methods=["POST"])
# def generate_video():
#     try:
#         input_text = request.json.get("text", "")
#         if not input_text:
#             return jsonify({"error": "Text is missing"}), 400
        
#         parse_input_text = nlp_pipeline(input_text, " ")
#         # Create GIF and convert it to a video
#         gif_path = create_animated_gif(parse_input_text)
#         video_path = convert_gif_to_storytelling_video(gif_path, parse_input_text)

#         # Ensure the uploads/videos directory exists
#         os.makedirs(UPLOADS_FOLDER, exist_ok=True)

#         # Save the generated video with a timestamped filename
#         timestamp = int(time.time())
#         video_filename = f"generated_video_{timestamp}.mp4"
#         final_video_path = os.path.join(UPLOADS_FOLDER, video_filename)
#         os.rename(video_path, final_video_path)

#         logger.info(f"Generated video path: {final_video_path}")

#         # Return the correct video path for the frontend
#         return jsonify({"video_path": f"/uploads/videos/{video_filename}"}), 200

#     except Exception as e:
#         logger.error(f"Error generating video: {e}")
#         return jsonify({"error": f"An internal error occurred: {str(e)}"}), 500


# ------------------------------------backup route if the code gets lost ------------------------------







# -------------------------------------------------------DONT USE THIS ROUTES HAVING MAJOR ROUTING ISSUES dont uncomment this code ------------------------







# Test Route to see if it works 


# from flask import jsonify



# @main.route("/generate_video", methods=["POST"])
# def generate_video():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file part"}), 400  # Return JSON with error message

#     file = request.files['file']
#     if file.filename == '' or not allowed_file(file.filename):
#         return jsonify({"error": "Invalid file type"}), 400  # Return JSON with error message

#     # Ensure the filename is safe
#     filename = secure_filename(file.filename)
#     filepath = os.path.join('F:\\100x_enginners_hackathon_genai\\uploads\\videos', filename)
#     file.save(filepath)

#     try:
#         # Step 1: Extract input text from the request
#         input_text = request.json.get("text", "")
#         if not input_text or not isinstance(input_text, str):
#             return jsonify({"error": "Invalid or missing text input"}), 400  # JSON error response

#         logger.debug(f"Input text received: {input_text}")

#         # Step 2: Parse input text using an NLP pipeline
#         try:
#             parsed_data = nlp_pipeline(input_text, "")  # Your ML model processes the text
#             logger.debug(f"Parsed data: {parsed_data}")
#         except Exception as e:
#             logger.error(f"Error in NLP pipeline: {e}")
#             return jsonify({"error": "Failed to process text input"}), 500  # JSON error response

#         # Ensure parsed_data has the required structure
#         if not isinstance(parsed_data, dict) or not all(key in parsed_data for key in ["categories", "values", "text"]):
#             logger.error(f"Unexpected parsed_data format: {parsed_data}")
#             return jsonify({"error": "Internal processing error"}), 500  # JSON error response

#         # Step 3: Generate the first video (existing implementation)
#         try:
#             # Generate a GIF and convert it into a storytelling video
#             gif_path = create_animated_gif(input_text)
#             logger.debug(f"Generated GIF path: {gif_path}")

#             video_path = convert_gif_to_storytelling_video(gif_path, input_text)
#             logger.debug(f"Generated first video path: {video_path}")
#         except Exception as e:
#             logger.error(f"Error generating first video: {e}")
#             return jsonify({"error": "Failed to generate first video"}), 500  # JSON error response

#         # Step 4: Generate the second video using the new function (create_scenario_based_infographic_video)
#         try:
#             # Use the create_scenario_based_infographic_video function to generate the second video
#             create_scenario_based_infographic_video()

#             # Assuming the final video is saved with the correct file name after this function call
#             second_video_path = "F:\\100x_enginners_hackathon_genai\\uploads\\videos\\final_infographic_video.mp4"
#             logger.debug(f"Generated second video path: {second_video_path}")
#         except Exception as e:
#             logger.error(f"Error generating second video: {e}")
#             return jsonify({"error": "Failed to generate second video"}), 500  # JSON error response

#         # Step 5: Save both videos in the UPLOADS_FOLDER and generate response
#         os.makedirs(UPLOADS_FOLDER, exist_ok=True)  # Ensure the folder exists
#         timestamp = int(time.time())

#         # Save the first video with a unique filename
#         first_video_filename = f"generated_video_1_{timestamp}.mp4"
#         first_video_final_path = os.path.join(UPLOADS_FOLDER, first_video_filename)
#         os.rename(video_path, first_video_final_path)

#         # Save the second video with a unique filename
#         second_video_filename = f"generated_video_2_{timestamp}.mp4"
#         second_video_final_path = os.path.join(UPLOADS_FOLDER, second_video_filename)
#         os.rename(second_video_path, second_video_final_path)

#         # Return the file paths for both videos in the response
#         return jsonify({
#             "first_video_path": f"/uploads/videos/{first_video_filename}",
#             "second_video_path": f"/uploads/videos/{second_video_filename}"
#         }), 200

#     except Exception as e:
#         # Handle unexpected errors and log them
#         logger.error(f"Unexpected error: {e}")
#         return jsonify({"error": "An unexpected error occurred"}), 500  # JSON error response


# second test route testing ---------------------------failed this fcuntionality route dont use it 

# @main.route("/generate_video", methods=["POST"])
# def generate_video():
#     try:
#         # Step 1: Extract input text
#         input_text = request.json.get("text", "")
#         if not input_text or not isinstance(input_text, str):
#             return jsonify({"error": "Invalid or missing text input"}), 400

#         logger.debug(f"Input text received: {input_text}")

#         # Step 2: Parse input text using the ML pipeline
#         try:
#             parsed_data = nlp_pipeline(input_text, "")  # Your ML model processes the text
#             logger.debug(f"Parsed data: {parsed_data}")
#         except Exception as e:
#             logger.error(f"Error in NLP pipeline: {e}")
#             return jsonify({"error": "Failed to process text input"}), 500

#         # Ensure parsed_data has the required structure
#         if not isinstance(parsed_data, dict) or not all(key in parsed_data for key in ["categories", "values", "text"]):
#             logger.error(f"Unexpected parsed_data format: {parsed_data}")
#             return jsonify({"error": "Internal processing error"}), 500

#         # Step 3: Generate an animated GIF using the parsed data
#         try:
#             gif_path = create_animated_gif(input_text)  # Use your existing function
#             logger.debug(f"Generated GIF path: {gif_path}")
#         except Exception as e:
#             logger.error(f"Error generating GIF: {e}")
#             return jsonify({"error": "Failed to generate GIF"}), 500

#         # Step 4: Convert the GIF to a video
#         try:
#             video_path = convert_gif_to_storytelling_video(gif_path, input_text)  # Use your existing function
#             logger.debug(f"Generated video path: {video_path}")
#         except Exception as e:
#             logger.error(f"Error converting GIF to video: {e}")
#             return jsonify({"error": "Failed to convert GIF to video"}), 500

#         # Step 5: Save the video and respond with the file path
#         os.makedirs(UPLOADS_FOLDER, exist_ok=True)
#         timestamp = int(time.time())
#         video_filename = f"generated_video_{timestamp}.mp4"
#         final_video_path = os.path.join(UPLOADS_FOLDER, video_filename)

#         # Ensure the final video path is unique
#         counter = 1
#         while os.path.exists(final_video_path):
#             video_filename = f"generated_video_{timestamp}_{counter}.mp4"
#             final_video_path = os.path.join(UPLOADS_FOLDER, video_filename)
#             counter += 1

#         os.rename(video_path, final_video_path)
#         shutil.move(final_video_path, UPLOADS_FOLDER)

#         return jsonify({"video_path": f"/uploads/videos/{video_filename}"}), 200

#     except Exception as e:
#         logger.error(f"Unexpected error: {e}")
#         return jsonify({"error": "An unexpected error occurred"}), 500