//  Multi Model Script For Custom Data Storytelling Video Generation 


function normalizeVideoPath(path) {
    // Remove any duplicate 'videos' folders in the path
    path = path.replace(/videos\/videos/, 'videos');
    // Ensure path starts with /uploads/
    if (!path.startsWith('/uploads/')) {
        path = '/uploads/' + path.replace(/^\/+/, '');
    }
    return path;
}

function showError(message, details = '') {
    const errorContainer = document.getElementById('errorContainer');
    const errorMessage = document.getElementById('errorMessage');
    const debugInfo = document.getElementById('debugInfo');
    
    errorMessage.textContent = message;
    if (details) {
        debugInfo.textContent = `Debug Info: ${details}`;
        debugInfo.style.display = 'block';
    }
    errorContainer.style.display = 'block';
    document.getElementById('videoContainer').style.display = 'none';
}

document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const fileInput = document.getElementById('data_file');
    const file = fileInput.files[0];
    const allowedTypes = ['text/csv', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'text/plain'];
    
    if (!file) {
        showError('Please select a file.');
        return;
    }

    if (!allowedTypes.includes(file.type)) {
        showError('Invalid file type. Please upload a CSV, XLSX, or TXT file.');
        return;
    }

    const formData = new FormData(this);
    const prompt = document.getElementById('prompt').value;
    formData.append('prompt', prompt);

    // Reset UI states
    document.getElementById('loadingSpinner').style.display = 'block';
    document.getElementById('videoContainer').style.display = 'none';
    document.getElementById('errorContainer').style.display = 'none';
    document.getElementById('debugInfo').style.display = 'none';

    fetch('/process', {
        method: 'POST',
        body: formData,
        headers: {
            'Accept': 'application/json',
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('loadingSpinner').style.display = 'none';

        if (data.error) {
            showError(data.error);
            return;
        }

        if (!data.video_file) {
            showError('No video file path received from server.');
            return;
        }

        const videoUrl = normalizeVideoPath(data.video_file);
        const video = document.getElementById('generatedVideo');
        video.src = videoUrl;

        video.onerror = function() {
            showError(
                'Error loading video.',
                `Attempted to load video from: ${videoUrl}`
            );
        };

        video.onloadeddata = function() {
            document.getElementById('videoContainer').style.display = 'block';
            document.getElementById('errorContainer').style.display = 'none';
            document.getElementById('debugInfo').style.display = 'none';
        };

        document.getElementById('videoContainer').style.display = 'block';
    })
    .catch(error => {
        document.getElementById('loadingSpinner').style.display = 'none';
        showError(
            'An unexpected error occurred.',
            error.toString()
        );
    });
});
 