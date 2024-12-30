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
from .csv_to_video_helper_function import create_infographic_video, nlp_csv_to_video_pipeline , generate_video_from_images , add_auto_generated_audio_to_video, create_visualizations, select_visualization_method, read_data
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
import mimetypes
from flask import session
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
TEMP_FOLDER = Path('D:\\1OOx-enginners-hackathon-submission-2\\temp')
TEMP_DIRECTORY = os.path.abspath("temp")
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
# TEMP_FOLDER.mkdir(parents=True, exist_ok=True)

UPLOADS_FOLDER.mkdir(parents=True, exist_ok=True)
TEMP_FOLDER.mkdir(parents=True, exist_ok=True)
# session handling ----------------

# session_id = uuid.uuid4().hex  # Unique session identifier
# user_upload_folder = os.path.join(UPLOADS_FOLDER, session_id)
# os.makedirs(user_upload_folder, exist_ok=True)

# session handling ----------------

def allowed_data_file(filename):
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
    session_folder.mkdir(exist_ok=True)
    return session_id, session_folder

def cleanup_temp_files(file_paths):
    """Remove temporary files."""
    for path in file_paths:
        if path and os.path.exists(path):  # Check if path is valid and exists
            try:
                os.remove(path)
                logger.info(f"Temporary file {path} removed successfully.")
            except Exception as e:
                logger.error(f"Error removing temporary file {path}: {e}")


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


# CSV Video processing function to process the video 

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


@main.route("/")
def index():
    return render_template('index.html')

@main.route("/text-to-video")
def text_to_video():
    return render_template('text-to-video.html')

@main.route("/csv-to-video")
def csv_to_video():
    return render_template('test_csv_to_video.html') 

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
            # Invert the condition to simplify comparisons
            return jsonify({"error": "Unexpected parsed_data format"}), 500

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
    """Handle file upload and store the file path in the session."""
    temp_path = None  # Temporary path for the uploaded file

    try:
        # Validate if file is present in the request
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request."}), 400

        file = request.files['file']
        filename = file.filename

        logger.info(f"Uploaded file: {filename}")

        # Validate if a file is selected
        if filename == '':
            return jsonify({"error": "No file selected for upload."}), 400

        # Validate file extension
        if not allowed_data_file(filename):
            detected_extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else "None"
            return jsonify({
                "error": f"Invalid file type. Detected: {detected_extension}. Allowed: {', '.join(ALLOWED_EXTENSIONS_FOR_DATA_FILES)}."
            }), 400

        # Validate MIME type
        mime_type, _ = mimetypes.guess_type(filename)
        allowed_mime_types = [
            'text/csv',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        ]
        if mime_type is None or mime_type not in allowed_mime_types:
            logger.info(f"Invalid MIME type: {mime_type}")
            return jsonify({"error": "Invalid file type based on MIME type."}), 400

        # Save the file to the temporary directory
        secure_name = secure_filename(filename)
        temp_path = os.path.join(TEMP_FOLDER, secure_name)
        logger.info(f"Saving uploaded file to temporary location: {temp_path}")
        file.save(temp_path)

        # Store the file path in the session for later use
        session['uploaded_csv'] = os.path.join(UPLOADS_FOLDER, secure_name)
        logger.info(f"File path stored in session: {session.get('uploaded_csv')}")

        return jsonify({"success": True, "message": "File uploaded successfully"}), 200

    except Exception as e:
        logger.error(f"Unexpected error during file upload: {e}", exc_info=True)
        return jsonify({"error": "An unexpected error occurred during file upload."}), 500

    finally:
        # Do not clean up the temp_path here as it is needed for the next step.
        pass
    
@main.route("/generate_video_from_csv", methods=["POST"])
def generate_video_from_csv():
    try:
        # Check for file in the request
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        if file and allowed_data_file(file.filename):
            # Save the uploaded file
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOADS_FOLDER, filename)
            file.save(file_path)
            logger.debug(f"Uploaded file saved at: {file_path}")

            # Generate video
            final_video_path = create_infographic_video(file_path)
            if not final_video_path or not os.path.exists(final_video_path):
                logger.error("Video file was not generated successfully or path does not exist.")
                return jsonify({"error": "Failed to generate video"}), 500

            # Ensure unique video filename
            os.makedirs(UPLOADS_FOLDER, exist_ok=True)
            timestamp = int(time.time())
            video_filename = f"generated_video_from_csv_{timestamp}.mp4"
            destination_path = os.path.join(UPLOADS_FOLDER, video_filename)

            if os.path.abspath(final_video_path) != os.path.abspath(destination_path):
                try:
                    shutil.move(final_video_path, destination_path)
                except FileNotFoundError as e:
                    logger.error(f"FileNotFoundError while moving video: {e}")
                    return jsonify({"error": "Generated video file was not found"}), 500
                except PermissionError as e:
                    logger.error(f"PermissionError while moving video: {e}")
                    return jsonify({"error": "Permission denied while saving video"}), 500
                except Exception as e:
                    logger.error(f"Unexpected error while moving video: {e}")
                    return jsonify({"error": "Unexpected error occurred while saving video"}), 500

            logger.debug(f"Video successfully moved to: {destination_path}")

            # Return video URL
            return jsonify({"video_path": f"/outputs/{video_filename}"}), 200

        return jsonify({"error": "Invalid file format"}), 400

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500



@main.route('/outputs/<video_name>', methods=['GET'])
def serve_video(video_name):
    """Serve generated video file"""
    video_path = os.path.join(UPLOADS_FOLDER, secure_filename(video_name))
    if not os.path.exists(video_path):
        return jsonify({"error": "Video not found"}), 404
    return send_from_directory(UPLOADS_FOLDER, secure_filename(video_name))

@main.route('/video/<video_name>', methods=['GET'])
def show_video(video_name):
    """Show video in the template"""
    video_path = os.path.join(UPLOADS_FOLDER, secure_filename(video_name))
    if not os.path.exists(video_path):
        return jsonify({"error": "Video not found"}), 404
    return render_template('test_csv_to_video.html', video_url=url_for('main.serve_video'), video_name=video_name)
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