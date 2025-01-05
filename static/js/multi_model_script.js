document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const prompt = document.getElementById('prompt').value;
    formData.append('prompt', prompt);

    fetch('/process', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('errorMessage').textContent = data.error;
            document.getElementById('errorContainer').style.display = 'block';
            document.getElementById('videoContainer').style.display = 'none';
        } else {
            const videoUrl = `/uploads/${data.video_file}`;
            const video = document.getElementById('generatedVideo');
            video.src = videoUrl;
            document.getElementById('videoContainer').style.display = 'block';
            document.getElementById('errorContainer').style.display = 'none';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('errorMessage').textContent = 'An unexpected error occurred.';
        document.getElementById('errorContainer').style.display = 'block';
        document.getElementById('videoContainer').style.display = 'none';
    });
});