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



from flask import Blueprint, render_template, request, jsonify , send_file , send_from_directory , url_for
from .utils import nlp_pipeline, convert_gif_to_storytelling_video , create_animated_gif # Ensure correct import
import logging
import os
import shutil
import time
import uuid
from .csv_to_video_helper_function import create_infographic_video , generate_video_from_images , add_auto_generated_audio_to_video, create_visualizations, select_visualization_method, read_data
from flask import Blueprint, render_template, request, jsonify, send_file, send_from_directory, url_for
from werkzeug.utils import secure_filename
import os
import logging
import uuid
import time
import shutil
from functools import wraps
from pathlib import Path
from werkzeug.utils import secure_filename
import os
import datetime
from pathlib import Path

# from .second_utility import create_scenario_based_infographic_video , create_animated_pie_chart , parse_user_input , generate_audio_from_text, generate_narration, add_auto_generated_audio_to_video
# from  .text_processing import nlp_pipeline
# from  .gif_animation_creation import create_animated_gif
# from  .data_storytelling_video_processing import convert_gif_to_storytelling_video
# from flask import Blueprint
# video_processing = Blueprint('video_processing', __name__)

main = Blueprint('main', __name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants and configurations
BASE_DIR = Path(__file__).resolve().parent
# Define path for static folder to serve video
UPLOADS_FOLDER = os.path.join(os.getcwd(), 'uploads', 'videos')
UPLOADS_FOLDER = Path('D:\\1OOx-enginners-hackathon-submission-2\\uploads\\videos')  # Convert to a Path object
# Define the base path for uploads
UPLOADS_DIRECTORY = os.path.abspath("uploads/videos")

# UPLOADS_FOLDER = 'D:\\1OOx-enginners-hackathon-submission-2\\uploads\\videos'

ALLOWED_EXTENSIONS_FOR_DATA_FILES = {'csv','xlsx' ,'txt', 'xls'}
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}  # add more if needed
TEMP_FOLDER = 'D:\\1OOx-enginners-hackathon-submission-2\\app\\temp'
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
# TEMP_FOLDER.mkdir(parents=True, exist_ok=True)

# UPLOADS_FOLDER.makedirs(parents=True, exist_ok=True)
# TEMP_FOLDER.makedirs(parents=True, exist_ok=True)
# session handling ----------------

# session_id = uuid.uuid4().hex  # Unique session identifier
# user_upload_folder = os.path.join(UPLOADS_FOLDER, session_id)
# os.makedirs(user_upload_folder, exist_ok=True)

# session handling ----------------

def allowed_file(filename):
    ALLOWED_EXTENSIONS_FOR_DATA_FILES = {'csv', 'xls', 'xlsx', 'txt'}
    ext = filename.rsplit('.', 1)[1].lower()
    return '.' in filename and ext in ALLOWED_EXTENSIONS_FOR_DATA_FILES


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class VideoProcessingError(Exception):
    """Custom exception for video processing errors"""
    pass

def error_handler(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except VideoProcessingError as e:
            logger.error(f"Video processing error: {str(e)}")
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return jsonify({"error": "An unexpected error occurred"}), 500
    return wrapper


def secure_file_path(filename):
    """Generate a secure file path with unique identifier"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    secure_name = secure_filename(filename)
    base_name, ext = os.path.splitext(secure_name)
    return f"{base_name}_{timestamp}_{unique_id}{ext}"

def create_user_session():
    """Create a unique session identifier and folder"""
    session_id = str(uuid.uuid4())
    session_folder = TEMP_FOLDER / session_id
    # session_folder.makedirs(exist_ok=True)
    return session_id, session_folder

def cleanup_temp_files(file_paths):
    """Clean up temporary files if they exist."""
    if file_paths is None or not file_paths:  # Check if file_paths is None or empty
        logger.info("No files to clean up.")
        return

    try:
        for path in file_paths:
            if os.path.exists(path):  # Ensure file exists before attempting to delete
                os.remove(path)
                logger.info(f"Cleaned up temporary file: {path}")
            else:
                logger.warning(f"File {path} does not exist.")
    except Exception as e:
        logger.error(f"Error cleaning up temporary files: {e}")

def get_temp_file_paths(temp_path):
    try:
        # Logic to gather file paths in temp_path
        file_paths = [os.path.join(temp_path, f) for f in os.listdir(temp_path) if os.path.isfile(os.path.join(temp_path, f))]
        
        if not file_paths:
            print(f"No files found in {temp_path}")
        
        return file_paths
    
    except Exception as e:
        print(f"Error retrieving temp files: {e}")
        return None  # In case of an error, you might want to handle it appropriately


def create_api_response(data=None, error=None, status=200):
    """Standardize API responses"""
    response = {
        "success": error is None,
        "data": data,
        "error": error
    }
    return jsonify(response), status


def create_infographic_video(file_path):
    df = read_data(file_path)
    summary = nlp_pipeline(df.to_string(index=False))
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


@main.route("/")
def index():
    return render_template('index.html')

@main.route("/text-to-video")
def text_to_video():
    return render_template('text-to-video.html')

@main.route("/csv-to-video")
def csv_to_video():
    return render_template('csv-to-video.html') 

@main.route('/uploads/videos/<filename>',methods=['GET'])
def uploaded_file(filename):
    return send_from_directory(UPLOADS_FOLDER, filename)

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
# Route for file upload and infographic video generation
@main.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and video generation"""  
    temp_path = None
    final_video_path = None
    
    # file = request.files['file']
    # filename = file.filename
    # logger.info(f"Uploaded file: {filename}")
  

    try:
        # Validate file presence
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400


        file = request.files['file']
        filename = file.filename
        logger.info(f"Uploaded file: {filename}")
        # Validate filename
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
            
        # Validate file type
        if not allowed_file(file.filename):
            return jsonify({
                "error": "Invalid file type. Only CSV, XLS, and XLSX files are allowed."
            }), 400

        # Create secure file path
        secure_name = secure_file_path(file.filename)
        temp_path = TEMP_FOLDER / secure_name
        
        # Save uploaded file to temporary location
        logger.info(f"Saving uploaded file to temporary location: {temp_path}")
        file.save(temp_path)
        
        # Generate infographic video
        try:
            from .csv_to_video_helper_function import create_infographic_video
            final_video_path = create_infographic_video(str(temp_path))
            
            if not final_video_path:
                    logger.error("Video creation failed, no video path returned.")
                    raise VideoProcessingError("Failed to create infographic video")
            
            # Move to permanent storage and generate response
            video_name = os.path.basename(final_video_path)
            permanent_path = UPLOADS_FOLDER / video_name
            
            # Ensure we don't overwrite existing files
            if permanent_path.exists():
                base, ext = os.path.splitext(video_name)
                video_name = f"{base}_{uuid.uuid4().hex[:8]}{ext}"
                permanent_path = UPLOADS_FOLDER / video_name
            
            # Move the file to permanent storage
            os.rename(final_video_path, permanent_path)
            
            return jsonify({
                "success": True,
                "video_url": url_for('main.serve_video', video_name=video_name, _external=True)
            }), 200
            
        except Exception as e:
            logger.error(f"Error processing video: {e}")
            return jsonify({
                "error": "An error occurred while generating the video."
            }), 500
            
    except Exception as e:
        logger.error(f"Unexpected error during file upload: {e}")
        return jsonify({
            "error": "An unexpected error occurred during file processing."
        }), 500
        
    finally:
        # Clean up temporary files, if any
        file_paths = [temp_path, final_video_path]  # List of temporary files
        cleanup_temp_files(file_paths)  # Call cleanup with the list of paths
            

@main.route('/outputs/<video_name>')
def serve_video(video_name):
    """Serve generated video file"""
    video_path = UPLOADS_FOLDER / secure_filename(video_name)
    if not video_path.exists():
        return jsonify({"error": "Video not found"}), 404
    return send_from_directory(str(UPLOADS_FOLDER), secure_filename(video_name))

@main.route('/video/<video_name>')
def show_video(video_name):
    """Show video in the template"""
    # Validate video exists before rendering
    video_path = UPLOADS_FOLDER / secure_filename(video_name)
    if not video_path.exists():
        return jsonify({"error": "Video not found"}), 404
    return render_template('csv-to-video.html', video_name=video_name)

# Serve the generated video

# Old Route IN USEE ---------------------------------------------------------------

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