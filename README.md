# Our Hackathon MVP:

## DataVizAI

**![images](https://github.com/user-attachments/assets/e26aee53-96a6-4271-a28d-646419758071)**


# MVP Videos:

**coming soon ....**

## Project Overview:

Dataviz AI is an AI powered web application that enables users to generate animated infographic videos based on input  Data , text,files. This MVP leverages the Pexels API for video content and incorporates advanced natural language processing (NLP) techniques, including LangChain and stable diffusion techniques, to analyze and create visual impact

## Key Features:

1. **Text-to-Video Conversion**: Users can input text, and the application will generate a video based on the content of the text, making information more engaging and accessible.
   
2. **NLP Analysis**: The application performs sentiment analysis and semantic segmentation on the input text to better understand its context and meaning, ensuring that the generated video aligns with the user's intent.

3. **Video Generation**: The application uses the Pexels API to search for videos that match the processed text and returns a selection of video URLs, providing users with high-quality visual content.

4. **Logging**: The application logs responses from the Pexels API and OpenAI (if integrated) for debugging and analytics purposes, allowing for continuous improvement and monitoring of the application’s performance.


## Impact of the Product

The Dataviz AI is an AI powered web application  has the potential to significantly impact various sectors, including education, marketing, and content creation. By transforming textual information into engaging video content, it enhances the way information is consumed and understood. Here are some key impacts:

- **Enhanced Learning**: In educational settings, the ability to convert complex text into visual formats can aid in comprehension and retention, making learning more effective.

- **Marketing and Communication**: Businesses can leverage this tool to create promotional videos quickly, allowing for more dynamic and engaging marketing strategies that capture audience attention.

- **Accessibility**: By providing visual representations of textual information, the application can help make content more accessible to individuals with different learning styles or those who may struggle with reading.

- **Content Creation**: Content creators can streamline their workflow by generating videos from scripts or articles, saving time and resources while maintaining high-quality output.


## Technical Overview

1. **Frontend**: The application uses HTML, CSS, and JavaScript for the user interface, providing a seamless user experience.

2. **Backend**: The application is built using Flask, a Python web framework that allows for easy routing and handling of HTTP requests.

3. **NLP Libraries**: The application utilizes the following NLP libraries:
   - **TextBlob** for sentiment analysis, enabling the application to gauge the emotional tone of the input text.
   - **SpaCy** for semantic segmentation, which helps in understanding the structure and meaning of the text.
   - **NLTK** for text preprocessing, ensuring that the input text is clean and ready for analysis.
   - **Transformers** and **Hugging Face** for advanced NLP tasks.
   - **LangChain** for managing and chaining together different language models and tasks.

4. **API Integration**: The application integrates with the Pexels API for video content, allowing users to access a vast library of stock videos.


## Installation and Setup

1. Clone the repository: 
   ```bash
    https://github.com/Blacksujit/100X-Engineers-GenAI-Hackathon-Submission.git
   ```

2. Install the required packages: 
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key (if using OpenAI integration).
   - `PEXELS_API_KEY`: Your Pexels API key.
   - `GROQ_API_KEY`: Your Groq API key. 

4. Run the application: 
   ```bash
   python app.py
   ```

## Usage

1. Open a web browser and navigate to `http://localhost:2000`.
2. Input text in the text box on the homepage and click the "Generate Video" button.
3. The application will redirect you to a page displaying the generated video URLs.


## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Make your changes and commit them.
4. Push your branch to your forked repository.
5. Submit a pull request to the original repository.

## License

This project is licensed under the MIT License.
