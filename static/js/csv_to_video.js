// CSV File or any data file preview script after uploading in the input 

document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const noFileMessage = document.getElementById('noFileMessage');
    const csvPreview = document.getElementById('csvPreview');
    
    // Clear previous preview content
    document.getElementById('previewHeader').innerHTML = '';
    document.getElementById('previewBody').innerHTML = '';
    
    if (!file) {
        noFileMessage.style.display = 'block'; // Show "No file uploaded" message
        csvPreview.style.display = 'none'; // Hide preview table
    } else {
        noFileMessage.style.display = 'none'; // Hide "No file uploaded" message
        csvPreview.style.display = 'block'; // Show preview table

        const fileType = file.type;
        const fileName = file.name.toLowerCase();

        // Handle CSV files
        if (fileType === 'text/csv' || fileName.endsWith('.csv')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const contents = e.target.result;
                const rows = contents.split('\n').map(row => row.split(','));

                // Create table header from first row of the CSV
                const headers = rows[0];
                headers.forEach(header => {
                    const th = document.createElement('th');
                    th.textContent = header;
                    document.getElementById('previewHeader').appendChild(th);
                });

                // Create table rows from CSV data
                rows.slice(1).forEach(row => {
                    const tr = document.createElement('tr');
                    row.forEach(cell => {
                        const td = document.createElement('td');
                        td.textContent = cell;
                        tr.appendChild(td);
                    });
                    document.getElementById('previewBody').appendChild(tr);
                });
            };
            reader.readAsText(file);
        }

        // Handle XLSX files
        else if (fileType === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' || fileName.endsWith('.xlsx')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const data = e.target.result;
                const workbook = XLSX.read(data, { type: 'binary' });
                const sheetName = workbook.SheetNames[0];
                const sheet = workbook.Sheets[sheetName];
                const rows = XLSX.utils.sheet_to_json(sheet, { header: 1 });

                // Create table header from first row of the XLSX data
                const headers = rows[0];
                headers.forEach(header => {
                    const th = document.createElement('th');
                    th.textContent = header;
                    document.getElementById('previewHeader').appendChild(th);
                });

                // Create table rows from XLSX data
                rows.slice(1).forEach(row => {
                    const tr = document.createElement('tr');
                    row.forEach(cell => {
                        const td = document.createElement('td');
                        td.textContent = cell;
                        tr.appendChild(td);
                    });
                    document.getElementById('previewBody').appendChild(tr);
                });
            };
            reader.readAsBinaryString(file);
        }

        // Handle TXT files
        else if (fileType === 'text/plain' || fileName.endsWith('.txt')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const contents = e.target.result;
                const rows = contents.split('\n');

                // Create table header from the first row (just a placeholder for simplicity)
                const headers = ['Line Number', 'Content'];
                headers.forEach(header => {
                    const th = document.createElement('th');
                    th.textContent = header;
                    document.getElementById('previewHeader').appendChild(th);
                });

                // Create table rows for TXT file (display line number and content)
                rows.forEach((line, index) => {
                    const tr = document.createElement('tr');
                    const td1 = document.createElement('td');
                    td1.textContent = index + 1; // Line number
                    const td2 = document.createElement('td');
                    td2.textContent = line;
                    tr.appendChild(td1);
                    tr.appendChild(td2);
                    document.getElementById('previewBody').appendChild(tr);
                });
            };
            reader.readAsText(file);
        }
        
        else {
            alert('Unsupported file type. Please upload CSV, XLSX, or TXT files.');
        }
    }
});






// script to integrate and process and handle the data to the backend
// to generate the video from the csv file or any data file

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
    const ALLOWED_EXTENSIONS = ['csv', 'xlsx', 'xls'];
    const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

    // File Input Change Handler
    fileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            validateAndPreviewFile(file);
        }
    });

    // File Validation
    function validateAndPreviewFile(file) {
        const extension = file.name.split('.').pop().toLowerCase();
        
        if (!ALLOWED_EXTENSIONS.includes(extension)) {
            showNotification('Please upload a CSV, XLSX, or XLS file');
            fileInput.value = '';
            return false;
        }

        if (file.size > MAX_FILE_SIZE) {
            showNotification('File size should not exceed 10MB');
            fileInput.value = '';
            return false;
        }

        // Preview file content
        previewFile(file);
        return true;
    }

    // File Preview
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

            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to generate video');
            }

            // Update video player with the generated video
            resultVideo.src = data.video_url + `?t=${new Date().getTime()}`;
            resultVideo.style.display = 'block';
            resultContainer.classList.add('active');
            resultContainer.style.display = 'block';

            // Setup download button
            downloadBtn.href = data.video_url;
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