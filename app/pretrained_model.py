# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# Model Training and Saving script 
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------



# import os
# import pickle
# from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# # Set the TRANSFORMERS_CACHE environment variable
# os.environ['HF_HOME'] = "D:\\cahc_models_folder"

# # Verify the environment variable is set correctly
# print("TRANSFORMERS_CACHE:", os.environ['HF_HOME'])

# # Load the model and tokenizer with the cache_dir parameter
# model = AutoModelForSeq2SeqLM.from_pretrained('t5-small', cache_dir=os.environ['HF_HOME'])
# tokenizer = AutoTokenizer.from_pretrained('t5-small', cache_dir=os.environ['HF_HOME'])

# # Set the path for the models directory (outside the app directory)
# models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')

# # Ensure the models directory exists
# os.makedirs(models_dir, exist_ok=True)

# # Save the model and tokenizer as .pkl files in the models folder
# try:
#     with open(os.path.join(models_dir, 'model.pkl'), 'wb') as model_file:
#         pickle.dump(model, model_file)

#     with open(os.path.join(models_dir, 'tokenizer.pkl'), 'wb') as tokenizer_file:
#         pickle.dump(tokenizer, tokenizer_file)
# except PermissionError as e:
#     print(f"PermissionError: {e}")
#     print("Please check the directory permissions and try running the script with elevated permissions.")


# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# Model Training and Saving script 
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
# ---------------------------------------------------ONLY USED FOR MODEL TRAINING --------------------------------
