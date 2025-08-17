# Our Hackathon MVP:

## DataVizAI

**![images](https://github.com/user-attachments/assets/e26aee53-96a6-4271-a28d-646419758071)**

## Sample Frontend Landing Page:

![image](./assets-of-app/image.png)

# MVP Videos:

**coming soon ....**

## Project Overview:

Dataviz AI is an AI powered web application that enables users to generate animated infographic videos based on input  Data , text,files. This MVP leverages the transformers and pretrained genai models to convert ur idea into an datastorytelling video  and incorporates advanced natural language processing (NLP) techniques, including LangChain and stable diffusion techniques, to analyze and create visual impact.


## System-Architecture-diagram:


![System Architecture](project-system-design/system-design-mermaid.png)

## Key Features:

**1. Text-to-Video Conversion:** 

**Feature Description:** 

Users can input text, and the application generates a video that visually represents the content, making information more engaging and accessible , so elimination for ads , and upliftment for datastorytelling.


**2. Multimodal CSV+Prompt to Video:**

**Feature Description:** 

This feature combines CSV data with user-provided prompts to 
generate videos that are both data-driven and contextually rich.

**Process:**
 
 Users provide a CSV , txt etc file along with a textual prompt. The application analyzes the CSV data and the prompt to extract insights and generate a narrative. This narrative, along with the visualizations from the CSV data, is used to create a comprehensive video that tells a story based on the input data and context.

**3. CSV to Video Conversion:**

**Feature Description:** 

This feature allows users to upload CSV files containing numerical data, which the application processes to generate visual representations such as bar charts, pie charts, and other infographic elements.

**Process:**

 The application reads the CSV data, performs exploratory data analysis (EDA), and uses the insights to create visualizations. These visualizations are then compiled into a video format, providing a dynamic way to present data.

**4. Data Storytelling Pipeline:** 

Processes user-provided numerical data and contextual information to generate infographic videos, including feature extraction, data visualization, and contextual video retrieval.

**5. Logging and Debugging:** 

Logs responses from APIs and internal processes for debugging and analytics, allowing for continuous improvement and monitoring of the application’s performance.


## Impact of the Product:

***The Dataviz AI is an AI powered web application  has the potential to significantly impact various sectors, including education, marketing, and content creation. By transforming textual information into engaging video content, it enhances the way information is consumed and understood. Here are some key impacts:***

- **Enhanced Learning**:

 In educational settings, the ability to convert complex text into visual formats can aid in comprehension and retention, making learning more effective.

- **Marketing and Communication**: 

Businesses can leverage this tool to create promotional videos quickly, allowing for more dynamic and engaging marketing strategies that capture audience attention.

- **Accessibility**:

 By providing visual representations of textual information, the application can help make content more accessible to individuals with different learning styles or those who may struggle with reading.

- **Content Creation**:

 Content creators can streamline their workflow by generating videos from scripts or articles, saving time and resources while maintaining high-quality output.


## Technical Overview:

1. **Frontend**: The application uses HTML, CSS, and JavaScript for the user interface, providing a seamless user experience.

2. **Backend**: The application is built using Flask, a Python web framework that allows for easy routing and handling of HTTP requests.

3. **NLP Libraries**: The application utilizes the following NLP libraries:
   - **TextBlob** for sentiment analysis, enabling the application to gauge the emotional tone of the input text.
   - **SpaCy** for semantic segmentation, which helps in understanding the structure and meaning of the text.
   - **NLTK** for text preprocessing, ensuring that the input text is clean and ready for analysis.
   - **Transformers** and **Hugging Face** for advanced NLP tasks.
   - **LangChain** for managing and chaining together different language models and tasks.


## Installation and Setup:

1. Clone the repository: 
   ```bash
    https://github.com/Blacksujit/100X-Engineers-GenAI-Hackathon-Submission.git
   ```

2. Install the required packages: 
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application: 
   ```bash
   python app.py
   ```
 
## Future Enhancements:

1. **Expanded API Integration**: Further integration with additional APIs to enhance video content options and provide users with a broader selection of stock videos and multimedia resources.

2. **Improved NLP Capabilities**: Incorporate more advanced NLP models and techniques to improve text analysis and video generation accuracy.

3. **User Interface Enhancements**: Develop a more intuitive and user-friendly interface to improve user experience and accessibility.

4. **Scalability Improvements**: Optimize the application for better performance and scalability to handle larger datasets and more concurrent users.


## Usage

1. Open a web browser and navigate to `http://localhost:2000`.

2. On the Home Page u will se three cards each card is having an different feature so u can get a rid of it and use it!!

3. Start implemnting  ur bussiness  ideas into , data storytelling video and hop on to this journey which is full of  colors!!


## Contributing:

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Make your changes and commit them.
4. Push your branch to your forked repository.
5. Submit a pull request to the original repository.

## License

This project is licensed under the MIT License.

