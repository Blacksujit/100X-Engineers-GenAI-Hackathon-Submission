# import os
# import joblib
# from transformers import BartTokenizer, BartForConditionalGeneration
# import spacy
# import logging

# def save_models(model_name="facebook/bart-base", save_directory="models"):
#     if not os.path.exists(save_directory):
#         os.makedirs(save_directory)
    
#     # Load the tokenizer and model
#     tokenizer = BartTokenizer.from_pretrained(model_name)
#     model = BartForConditionalGeneration.from_pretrained(model_name)
    
#     # Save the tokenizer and model using joblib
#     joblib.dump(tokenizer, os.path.join(save_directory, "facebook_tokenizer_joblib.pkl"))
#     joblib.dump(model, os.path.join(save_directory, "facebook_model_joblib.pkl"))
    
#     # Load and save the spaCy model using joblib
#     nlp = spacy.load("en_core_web_sm")
#     joblib.dump(nlp, os.path.join(save_directory, "spacy_model_joblib.pkl"))
    
#     logging.info(f"Models saved to {save_directory}")

# # Call this function once to save the models
# save_models()