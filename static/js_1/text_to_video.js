 
const generateButton = document.getElementById('generateButton');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultContainer = document.getElementById('resultContainer');
const resultVideo = document.getElementById('resultVideo');
const errorContainer = document.getElementById('errorContainer');
const textInput = document.getElementById('textInput');

generateButton.addEventListener('click', async () => {
    const inputText = textInput.value.trim();
    
    if (!inputText) {
        showError('Please enter some text');
        return;
    }

    // Reset UI state
    hideError();
    showLoading();
    resultContainer.classList.remove('active');
    generateButton.disabled = true;

    try {
        const response = await fetch('/generate_video', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: inputText })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to generate video');
        }

        // Display the video
        resultVideo.src = data.video_path;
        resultContainer.classList.add('active');
        
    } catch (error) {
        showError(error.message || 'An error occurred while generating the video');
    } finally {
        hideLoading();
        generateButton.disabled = false;
    }
});

function showError(message) {
    errorContainer.innerHTML = `<div class="error-message">${message}</div>`;
}

function hideError() {
    errorContainer.innerHTML = '';
}

function showLoading() {
    loadingSpinner.classList.add('active');
}

function hideLoading() {
    loadingSpinner.classList.remove('active');
}
 