document.addEventListener('DOMContentLoaded', () => {
    const generateButton = document.getElementById('generateButton');
    const progressBar = document.getElementById('progress');
    const resultContainer = document.getElementById('resultContainer');
    const resultVideo = document.getElementById('resultVideo');
    const errorContainer = document.getElementById('errorContainer');
    const downloadBtn = document.getElementById('downloadBtn');
    const textInput = document.getElementById('textInput');
    const progressBarContainer = document.querySelector('.progress-bar');

    generateButton.addEventListener('click', async () => {
        const inputText = textInput.value.trim();
        if (!inputText) {
            showNotification('Please enter some text');
            return;
        }

        progressBarContainer.style.display = 'block';
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

            resultVideo.src = data.video_path + `?t=${new Date().getTime()}`;
            resultVideo.style.display = 'block';
            resultContainer.classList.add('active');
            downloadBtn.addEventListener('click', () => {
                const link = document.createElement('a');
                link.href = data.video_path;
                link.download = 'video.mp4';
                link.click();
            });

        } catch (error) {
            showNotification(error.message || 'An error occurred while generating the video');
        } finally {
            hideLoading();
            generateButton.disabled = false;
        }
    });

    function showNotification(message) {
        errorContainer.innerText = message;
        errorContainer.classList.add('show');
        setTimeout(() => {
            errorContainer.classList.remove('show');
        }, 3000);
    }

    function showLoading() {
        progressBar.style.width = '50%';
    }

    function hideLoading() {
        progressBar.style.width = '100%';
        setTimeout(() => {
            progressBarContainer.style.display = 'none';
        }, 500);
    }
});
