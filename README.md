# MVP Video



https://github.com/user-attachments/assets/eac1daef-4fd1-4355-95c9-4a0f0dab28aa



## some generated inforgraphcis by our MVP:



https://github.com/user-attachments/assets/46526010-1cab-4e09-97ea-a787d8a5ea59



https://github.com/user-attachments/assets/0014f38f-486d-4d31-a93c-a0e74515931f



https://github.com/user-attachments/assets/8c631010-4d3f-4e0e-9a9d-b00006173f7f



https://github.com/user-attachments/assets/16c78aa8-6636-4297-8ccc-325677c56a68







# Project Overview:

This project is a Flask-based web application that allows users to generate animated infographic videos based on input text. The application leverages the Pexels API for video content and incorporates natural language processing (NLP) techniques to analyze and transform the input text into a suitable format for video generation.

# Features:

1. **Text-to-Video Conversion**: Users can input text, and the application will generate a video based on the content of the text.
2. **NLP Analysis**: The application performs sentiment analysis and semantic segmentation on the input text to better understand its context and meaning.
3. **Video Generation**: The application uses the Pexels API to search for videos that match the processed text and returns a selection of video URLs.
4. **Logging**: The application logs responses from the Pexels API and OpenAI (if integrated) for debugging and analytics purposes.

# Technical Details:

1. **Backend**: The application is built using Flask, a Python web framework.
2. **NLP Libraries**: The application utilizes the following NLP libraries:
	* TextBlob for sentiment analysis
	* Spacy for semantic segmentation
	* NLTK for text preprocessing
    *transformers
    *huggingface
    *langchain
3. **API Integration**: The application integrates with the Pexels API for video content.
4. **Frontend**: The application uses HTML, CSS, and JavaScript for the user interface.

# Installation and Setup:

1. Clone the repository: `git clone https://github.com/Blacksujit/100X-Enginnerres-Hackathon-Submission`

2. Install the required packages: `pip install -r requirements.txt`
3. Set up the environment variables:
	* `OPENAI_API_KEY`: Your OpenAI API key (if using OpenAI integration)
	* `PEXELS_API_KEY`: Your Pexels API key
4. Run the application: `python app.py`

# Usage:

1. Open a web browser and navigate to `http://localhost:2000`
2. Input text in the text box on the homepage and click the "Generate Video" button.
3. The application will redirect you to a page displaying the generated video URLs.

# Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository
2. Create a new branch for your feature or fix
3. Make your changes and commit them
4. Push your branch to your forked repository
5. Submit a pull request to the original repository

# License

This project is licensed under the MIT License.
