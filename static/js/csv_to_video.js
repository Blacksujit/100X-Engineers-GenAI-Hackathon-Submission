
// script to integrate and process and handle the data to the backend
// to generate the video from the csv file or any data file


document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const generateButton = document.getElementById('generateButton');
    const progressBar = document.getElementById('progress');
    const resultContainer = document.getElementById('resultContainer');
    const resultVideo = document.getElementById('resultVideo');
    const errorContainer = document.getElementById('errorContainer');
    const downloadBtn = document.getElementById('downloadBtn');
    const filePreview = document.getElementById('filePreview');
    const progressBarContainer = document.querySelector('.progress-bar');

    // Constants
    const ALLOWED_EXTENSIONS = ['csv', 'xlsx', 'xls', 'txt'];
    const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

    // File Input Change Handler
    fileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            validateAndPreviewFile(file);
        }
    });

    // Validate and Preview File
    function validateAndPreviewFile(file) {
        const extension = file.name.split('.').pop().toLowerCase();
        const ALLOWED_MIME_TYPES = [
            'text/csv',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.ms-excel',
            'text/plain'
        ];
    
        if (!ALLOWED_MIME_TYPES.includes(file.type) && !ALLOWED_EXTENSIONS.some(ext => file.name.toLowerCase().endsWith(ext))) {
            showNotification('Unsupported file type. Please upload CSV, XLSX, or TXT files.');
            return false;
        }
    
        if (file.size > MAX_FILE_SIZE) {
            showNotification('File size should not exceed 10MB');
            return false;
        }
    
        previewFile(file);
        return true;
    }

    // Preview the selected file
    function previewFile(file) {
        const reader = new FileReader();

        reader.onload = (e) => {
            filePreview.innerHTML = `
                <div class="preview-info">
                    <p class="file-name">File: ${file.name}</p>
                    <p class="file-size">Size: ${(file.size / 1024).toFixed(2)} KB</p>
                </div>
            `;
            filePreview.style.display = 'block';
            generateButton.disabled = false;
        };

        reader.onerror = () => {
            showNotification('Error reading file');
            filePreview.style.display = 'none';
            generateButton.disabled = true;
        };

        reader.readAsDataURL(file);
    }

    // Form Submit Handler
    uploadForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const file = fileInput.files[0];
        if (!file) {
            showNotification('Please select a file');
            return;
        }

        if (!validateAndPreviewFile(file)) {
            return;
        }

        progressBarContainer.style.display = 'block';
        showLoading();
        resultContainer.classList.remove('active');
        generateButton.disabled = true;

        try {
            const formData = new FormData();
            formData.append('file', file);

            // Upload file to the /upload route
            const uploadResponse = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const uploadData = await uploadResponse.json();
            if (!uploadResponse.ok) {
                throw new Error(uploadData.error || 'Failed to upload file');
            }

            // Once the file is uploaded, call the /generate_video_from_csv route
            const generateResponse = await fetch('/generate_video_from_csv', {
                method: 'POST',
                body: formData
            });

            const generateData = await generateResponse.json();

            if (!generateResponse.ok) {
                throw new Error(generateData.error || 'Failed to generate video');
            }

            // Update video player with the generated video
            const videoUrl = generateData.video_path; // This is the video URL returned by Flask
            resultVideo.src = videoUrl + `?t=${new Date().getTime()}`;
            resultVideo.style.display = 'block';
            resultContainer.classList.add('active');
            resultContainer.style.display = 'block';

            // Setup download button
            downloadBtn.href = videoUrl;
            downloadBtn.style.display = 'block';

        } catch (error) {
            showNotification(error.message || 'An error occurred while generating the video');
        } finally {
            hideLoading();
            generateButton.disabled = false;
        }
    });

    // Notification Handler
    function showNotification(message) {
        errorContainer.innerText = message;
        errorContainer.style.display = 'block';
        setTimeout(() => {
            errorContainer.style.display = 'none';
        }, 3000);
    }

    // Loading State Handlers
    function showLoading() {
        progressBar.style.width = '50%';
        generateButton.disabled = true;
    }

    function hideLoading() {
        progressBar.style.width = '100%';
        setTimeout(() => {
            progressBarContainer.style.display = 'none';
            progressBar.style.width = '0%';
        }, 500);
        generateButton.disabled = false;
    }

    // Drag and Drop Handlers
    const dropZone = document.querySelector('.file-upload-wrapper');

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');

        const file = e.dataTransfer.files[0];
        if (file) {
            fileInput.files = e.dataTransfer.files;
            validateAndPreviewFile(file);
        }
    });
});

//  direct file and video parsing code 

// document.addEventListener("DOMContentLoaded", function () {
//     const uploadForm = document.getElementById("uploadForm");
//     const fileInput = document.getElementById("fileInput");
//     const generateButton = document.getElementById("generateButton");
//     const errorContainer = document.getElementById("errorContainer");
//     const progressBar = document.getElementById("progress");
//     const resultContainer = document.getElementById("resultContainer");
//     const resultVideo = document.getElementById("resultVideo");
//     const downloadBtn = document.getElementById("downloadBtn");

//     // Helper function to show errors
//     function showError(message) {
//         errorContainer.innerHTML = `<p class="text-red-500">${message}</p>`;
//         errorContainer.style.display = "block";
//     }

//     // Helper function to hide error messages
//     function hideError() {
//         errorContainer.style.display = "none";
//     }

//     // Function to handle video creation
//     function handleFileUpload(event) {
//         event.preventDefault();

//         hideError();

//         const file = fileInput.files[0];
//         if (!file) {
//             showError("Please select a file to upload.");
//             return;
//         }

//         // Show progress bar and disable button
//         generateButton.disabled = true;
//         progressBar.style.width = "0%";
//         resultContainer.style.display = "none";

//         const formData = new FormData(uploadForm);

//         const request = new XMLHttpRequest();
//         request.open("POST", uploadForm.action, true);

//         request.upload.addEventListener("progress", function (event) {
//             if (event.lengthComputable) {
//                 const percent = (event.loaded / event.total) * 100;
//                 progressBar.style.width = `${percent}%`;
//             }
//         });

//         request.onload = function () {
//             if (request.status === 200) {
//                 const response = JSON.parse(request.responseText);

//                 if (response.video_url) {
//                     // Display video
//                     resultContainer.style.display = "block";
//                     resultVideo.src = response.video_url;
//                     downloadBtn.href = response.video_url;
//                 } else if (response.error) {
//                     showError(response.error);
//                 }
//             } else {
//                 showError("An error occurred during video generation.");
//             }

//             // Reset progress and button
//             generateButton.disabled = false;
//             progressBar.style.width = "0%";
//         };

//         request.onerror = function () {
//             showError("Network error occurred. Please try again.");
//             generateButton.disabled = false;
//             progressBar.style.width = "0%";
//         };

//         request.send(formData);
//     }

//     uploadForm.addEventListener("submit", handleFileUpload);
// });





// using the json implementation 


