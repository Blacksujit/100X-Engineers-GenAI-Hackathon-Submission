// Multi Model Script For Custom Data Storytelling Video Generation 
// Enhanced with CSV preview functionality and professional prompt management

// DOM Elements
const uploadContainer = document.getElementById('upload-container');
const fileInput = document.getElementById('file-input');
const previewContainer = document.getElementById('preview-container');
const tableHeader = document.getElementById('table-header');
const tableBody = document.getElementById('table-body');
const generateButton = document.getElementById('generate-button');
const videoContainer = document.getElementById('video-container');
const videoPlayer = document.getElementById('video-player');

const searchInput = document.getElementById('table-search');
const rowCountElement = document.getElementById('row-count');
const columnCountElement = document.getElementById('column-count');
const downloadCsvBtn = document.getElementById('download-csv');
const downloadVideoBtn = document.getElementById('download-video');
const progressBar = document.querySelector('.progress-bar-fill');
const progressText = document.querySelector('.progress-text');
const promptInput = document.getElementById('prompt-input');
const wordCount = document.getElementById('wordCount');
const promptWarning = document.getElementById('promptWarning');

// State management
let currentData = [];
let filteredData = [];
let currentFile = null;

// Constants
const allowedExtensions = ['csv', 'xlsx', 'xls', 'txt'];
const maxSize = 10 * 1024 * 1024; // 10MB
const MAX_WORDS = 25;



// Event Listeners
uploadContainer.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadContainer.style.borderColor = '#007bff';
});

uploadContainer.addEventListener('dragleave', () => {
    uploadContainer.style.borderColor = '#ccc';
});

uploadContainer.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadContainer.style.borderColor = '#ccc';
    const file = e.dataTransfer.files[0];
    handleFile(file);
});

uploadContainer.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    handleFile(file);
});

// Prompt input handling with strict word count limit
promptInput.addEventListener('input', (e) => {
    const prompt = e.target.value;
    const wordCountValue = countWords(prompt);
    
    // Update word count display
    wordCount.textContent = `${wordCountValue}/${MAX_WORDS}`;
    
    // Simple styling logic - no notifications
    if (wordCountValue > MAX_WORDS) {
        // Prevent typing by truncating
        e.target.value = truncateToWordLimit(prompt);
        wordCount.textContent = `${MAX_WORDS}/${MAX_WORDS}`;
        
        // Red styling
        wordCount.parentElement.classList.add('exceeded');
        promptWarning.parentElement.classList.add('exceeded');
        promptWarning.textContent = 'Keep it concise!';
        
        // Remove success styling
        wordCount.parentElement.classList.remove('success');
        promptWarning.parentElement.classList.remove('success');
    } else {
        // Remove red styling
        wordCount.parentElement.classList.remove('exceeded');
        promptWarning.parentElement.classList.remove('exceeded');
        
        if (wordCountValue >= 3) {
            // Green styling
            wordCount.parentElement.classList.add('success');
            promptWarning.parentElement.classList.add('success');
            promptWarning.textContent = 'Good length!';
        } else {
            // Normal styling
            wordCount.parentElement.classList.remove('success');
            promptWarning.parentElement.classList.remove('success');
            promptWarning.textContent = 'Minimum 3 words required';
        }
    }
});



// Utility Functions
function countWords(text) {
    if (!text.trim()) return 0;
    return text.trim().split(/\s+/).filter(word => word.length > 0).length;
}

function truncateToWordLimit(text) {
    const words = text.trim().split(/\s+/);
    return words.slice(0, MAX_WORDS).join(' ');
}

function validatePrompt(wordCount) {
    return wordCount >= 3 && wordCount <= MAX_WORDS;
}







function showWordLimitExceededNotification() {
    Swal.fire({
        title: 'Word Limit Exceeded!',
        text: `Please keep your prompt to ${MAX_WORDS} words maximum for better results.`,
        icon: 'warning',
        confirmButtonText: 'Got it!',
        confirmButtonColor: '#99FF66',
        background: '#1f2937',
        color: '#ffffff',
        timer: 3000,
        timerProgressBar: true,
        toast: true,
        position: 'top',
        showClass: {
            popup: 'animate__animated animate__fadeInDown'
        },
        hideClass: {
            popup: 'animate__animated animate__fadeOutUp'
        }
    });
}

function showFileRequiredNotification() {
    Swal.fire({
        title: 'File Required!',
        text: 'Please upload a data file first to generate your video.',
        icon: 'info',
        confirmButtonText: 'Upload File',
        confirmButtonColor: '#99FF66',
        background: '#1f2937',
        color: '#ffffff',
        timer: 4000,
        timerProgressBar: true,
        toast: true,
        position: 'center',
        showClass: {
            popup: 'animate__animated animate__fadeInDown'
        },
        hideClass: {
            popup: 'animate__animated animate__fadeOutUp'
        }
    }).then((result) => {
        if (result.isConfirmed) {
            // Scroll to upload section and highlight it
            const uploadSection = document.querySelector('.upload-section');
            
            if (uploadSection) {
                // Smooth scroll to upload section with offset
                const offset = 80; // Account for navbar height
                const elementPosition = uploadSection.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - offset;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
                
                // Add a subtle highlight effect
                uploadSection.style.boxShadow = '0 0 20px rgba(153, 255, 102, 0.3)';
                setTimeout(() => {
                    uploadSection.style.boxShadow = '';
                }, 1000);
            }
        }
    });
}

function showPromptRequiredNotification() {
    Swal.fire({
        title: 'Prompt Required!',
        text: 'Please enter a creative prompt (3-25 words) to generate your video.',
        icon: 'info',
        confirmButtonText: 'Add Prompt',
        confirmButtonColor: '#99FF66',
        background: '#1f2937',
        color: '#ffffff',
        timer: 4000,
        timerProgressBar: true,
        toast: true,
        position: 'center',
        showClass: {
            popup: 'animate__animated animate__fadeInDown'
        },
        hideClass: {
            popup: 'animate__animated animate__fadeOutUp'
        }
    }).then((result) => {
        if (result.isConfirmed) {
            // Scroll to prompt section and focus the input
            const promptSection = document.querySelector('.prompt-section');
            const promptInput = document.getElementById('prompt-input');
            
            if (promptSection && promptInput) {
                // Smooth scroll to prompt section with offset
                const offset = 80; // Account for navbar height
                const elementPosition = promptSection.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - offset;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
                
                // Focus the input field after a short delay
                setTimeout(() => {
                    promptInput.focus();
                    // Add a subtle highlight effect
                    promptSection.style.boxShadow = '0 0 20px rgba(153, 255, 102, 0.3)';
                    setTimeout(() => {
                        promptSection.style.boxShadow = '';
                    }, 1000);
                }, 500);
            }
        }
    });
}

function showSuccessNotification(message) {
    Swal.fire({
        title: 'Success!',
        text: message,
        icon: 'success',
        confirmButtonText: 'Great!',
        confirmButtonColor: '#99FF66',
        background: '#1f2937',
        color: '#ffffff',
        timer: 3000,
        timerProgressBar: true,
        toast: true,
        position: 'top-end',
        showConfirmButton: false
    });
}

function showErrorNotification(message) {
    Swal.fire({
        title: 'Error!',
        text: message,
        icon: 'error',
        confirmButtonText: 'OK',
        confirmButtonColor: '#ef4444',
        background: '#1f2937',
        color: '#ffffff',
        timer: 5000,
        timerProgressBar: true,
        toast: true,
        position: 'top-end'
    });
}











// File handling
async function handleFile(file) {
    try {
    if (!file) {
            throw new Error('No file selected');
        }

        if (file.size > maxSize) {
            throw new Error('File size too large. Please upload a file smaller than 10MB.');
        }

        const fileExtension = file.name.split('.').pop().toLowerCase();

        if (!allowedExtensions.includes(fileExtension)) {
            throw new Error(`Invalid file type. Only ${allowedExtensions.join(', ')} files are allowed. You uploaded a .${fileExtension} file.`);
        }

        currentFile = file;

        let data;
        if (fileExtension === 'csv' || fileExtension === 'txt') {
            data = await parseCSV(file);
        } else {
            data = await parseExcel(file);
        }

        // Store the full dataset
        currentData = data;
        filteredData = [...data];

        // Enable download CSV button
        downloadCsvBtn.disabled = false;

        displayPreview(data);
        previewContainer.style.display = 'block';
        previewContainer.classList.add('active');

        // Show success message
        showSuccessNotification('File loaded successfully!');

        // File loaded successfully - no need to check button state

    } catch (error) {
        showErrorNotification(error.message);
    }
}

function parseCSV(file) {
    return new Promise((resolve) => {
        Papa.parse(file, {
            header: true,
            complete: (results) => resolve(results.data),
            skipEmptyLines: true
        });
    });
}

async function parseExcel(file) {
    const arrayBuffer = await file.arrayBuffer();
    const workbook = XLSX.read(arrayBuffer, { type: 'array' });
    const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
    return XLSX.utils.sheet_to_json(firstSheet);
}

function updateDataStats(data) {
    const rowCount = data.length;
    const columnCount = data.length > 0 ? Object.keys(data[0]).length : 0;
    rowCountElement.querySelector('span').textContent = `${rowCount.toLocaleString()} rows`;
    columnCountElement.querySelector('span').textContent = `${columnCount} columns`;
}

function filterData(searchTerm) {
    if (!searchTerm) {
        filteredData = [...currentData];
        displayPreview(currentData);
        return;
    }

    const term = searchTerm.toLowerCase();
    filteredData = currentData.filter(row => 
        Object.values(row).some(value => 
            String(value).toLowerCase().includes(term)
        )
    );
    displayPreview(filteredData);
}

function displayPreview(data) {
    if (!data.length) {
        showErrorNotification('No data to display');
        return;
    }

    tableHeader.innerHTML = '';
    tableBody.innerHTML = '';

    // Create and populate header
    const headers = Object.keys(data[0]);
    headers.forEach(header => {
        const th = document.createElement('th');
        th.textContent = header;
        th.addEventListener('mouseover', () => highlightColumn(header));
        th.addEventListener('mouseout', () => removeColumnHighlight());
        tableHeader.appendChild(th);
    });

    // Create and populate body
    data.forEach((row, index) => {
        const tr = document.createElement('tr');
        tr.style.animation = `fadeIn 0.3s ease forwards ${index * 0.03}s`;
        
        headers.forEach(header => {
            const td = document.createElement('td');
            td.textContent = row[header] || '';
            td.dataset.column = header;
            tr.appendChild(td);
        });
        
        tableBody.appendChild(tr);
    });

    updateDataStats(currentData);
}

// Column highlight function
function highlightColumn(header) {
    const cells = document.querySelectorAll(`td[data-column="${header}"]`);
    cells.forEach(cell => cell.dataset.highlighted = "true");
}

function removeColumnHighlight() {
    const cells = document.querySelectorAll('td[data-highlighted]');
    cells.forEach(cell => delete cell.dataset.highlighted);
}

// Progress bar updates
function updateProgress(percent) {
    if (progressBar) {
        progressBar.style.width = `${percent}%`;
    }
    if (progressText) {
        progressText.textContent = `${Math.round(percent)}%`;
    }
}

// Generate Video with Progress
generateButton.addEventListener('click', async () => {
    // Prevent multiple clicks during processing
    if (generateButton.classList.contains('loading')) {
        return;
    }

    try {
        // Check if file is uploaded
        if (!currentFile) {
            showFileRequiredNotification();
        return;
    }

        // Check if prompt is entered
        const prompt = promptInput.value.trim();
        const wordCountValue = countWords(prompt);
        
        if (!prompt || wordCountValue < 3) {
            showPromptRequiredNotification();
        return;
    }

        if (wordCountValue > MAX_WORDS) {
        return;
    }

        // Close any existing SweetAlert
        Swal.close();

        // Disable button and show loading state
        generateButton.classList.add('loading');
        generateButton.disabled = true;
        updateProgress(0);

        const formData = new FormData();
        formData.append('data_file', currentFile);
        formData.append('prompt', prompt);

        // Simulate progress updates (replace with real progress when available)
        const progressInterval = setInterval(() => {
            const currentWidth = parseInt(progressBar?.style.width) || 0;
            if (currentWidth < 90) {
                updateProgress(currentWidth + Math.random() * 10);
            }
        }, 500);

        const response = await fetch('/process', {
        method: 'POST',
        body: formData,
        headers: {
            'Accept': 'application/json',
        },
            credentials: 'include',
        });

        clearInterval(progressInterval);

        if (!response.ok) {
            const text = await response.text();
            throw new Error('Error generating video: ' + text);
        }

        const responseData = await response.json();

        if (responseData.error) {
            throw new Error(responseData.error);
        }

        updateProgress(100);
        
        videoPlayer.src = responseData.video_file;
        videoContainer.style.display = 'block';
        videoContainer.classList.add('active');

        // Enable download video button
        downloadVideoBtn.disabled = false;
        showSuccessNotification('Professional video generated successfully!');

    } catch (error) {
        showErrorNotification(error.message);
        updateProgress(0);
    } finally {
        // Re-enable button and remove loading state
        generateButton.classList.remove('loading');
        generateButton.disabled = false;
    }
});

// Search functionality
let searchTimeout;
searchInput.addEventListener('input', (e) => {
    clearTimeout(searchTimeout);
    const searchTerm = e.target.value;
    
    // Add loading class to search box
    searchInput.parentElement.classList.add('searching');
    
    searchTimeout = setTimeout(() => {
        filterData(searchTerm);
        searchInput.parentElement.classList.remove('searching');
    }, 300);
});

// Download CSV functionality
downloadCsvBtn.addEventListener('click', () => {
    if (!currentData.length) return;

    const headers = Object.keys(currentData[0]);
    const csvContent = [
        headers.join(','),
        ...currentData.map(row => headers.map(header => `"${row[header] || ''}"`).join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'data_export.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);

    showSuccess('CSV file downloaded successfully!');
});

// Download Video functionality
downloadVideoBtn.addEventListener('click', () => {
    const videoPath = videoPlayer.src;
    if (!videoPath) return;

    const link = document.createElement('a');
    link.href = videoPath;
    link.download = 'generated_video.mp4';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    showSuccess('Video download started!');
});

// Regenerate Video functionality
const regenerateBtn = document.getElementById('regenerate-video');
regenerateBtn.addEventListener('click', () => {
    // Add spinning animation to regenerate icon
    const icon = regenerateBtn.querySelector('.fa-sync-alt');
    icon.style.transform = 'rotate(360deg)';
    
    // Disable the button temporarily
    regenerateBtn.disabled = true;
    
    // Show a brief loading state
    regenerateBtn.classList.add('loading');
    
    // Add fade-out animation to current content
    const mainContainer = document.querySelector('.main-container');
    mainContainer.style.opacity = '0';
    
    setTimeout(() => {
        // Reset all states
        resetPageState();
        
        // Fade back in
        mainContainer.style.opacity = '1';
        
        // Reset button state
        regenerateBtn.disabled = false;
        regenerateBtn.classList.remove('loading');
        icon.style.transform = '';
        
        // Show success message
        showSuccessNotification('Ready for new video generation!');
    }, 500);
});

// Reset page state function
function resetPageState() {
    // Reset file input
    fileInput.value = '';
    
    // Reset data states
    currentData = [];
    filteredData = [];
    currentFile = null;
    
    // Clear table
    tableHeader.innerHTML = '';
    tableBody.innerHTML = '';
    
    // Reset search
    if (searchInput) {
        searchInput.value = '';
    }
    
    // Reset prompt
    if (promptInput) {
        promptInput.value = '';
        wordCount.textContent = '0/25';
        promptWarning.textContent = 'Keep it concise';
        promptWarning.style.color = 'rgba(255, 255, 255, 0.7)';
        
        // Remove styling classes
        wordCount.parentElement.classList.remove('exceeded', 'success');
        promptWarning.parentElement.classList.remove('exceeded', 'success');
    }
    
    // Reset stats
    if (rowCountElement) {
        rowCountElement.querySelector('span').textContent = '0 rows';
    }
    if (columnCountElement) {
        columnCountElement.querySelector('span').textContent = '0 columns';
    }
    
    // Reset progress
    updateProgress(0);
    
    // Hide sections
    previewContainer.style.display = 'none';
    previewContainer.classList.remove('active');
    videoContainer.style.display = 'none';
    videoContainer.classList.remove('active');
    
    // Reset video player
    videoPlayer.src = '';
    
    // Reset buttons - keep generate button enabled
    generateButton.classList.remove('loading', 'invalid-prompt', 'ready-to-generate');
    if (downloadCsvBtn) {
        downloadCsvBtn.disabled = true;
    }
    if (downloadVideoBtn) {
        downloadVideoBtn.disabled = true;
    }
    
    // Show and highlight upload section
    uploadContainer.style.display = 'block';
    uploadContainer.style.opacity = '0';
    
    // Smooth scroll to upload section
    uploadContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
    
    // Add highlight animation
    setTimeout(() => {
        uploadContainer.style.opacity = '1';
        uploadContainer.classList.add('highlight-upload');
        setTimeout(() => {
            uploadContainer.classList.remove('highlight-upload');
        }, 1000);
    }, 300);
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Initialize word count
    wordCount.textContent = '0/25';
    
    // Keep button enabled by default
    generateButton.disabled = false;
    
    // Add enhanced styling for button states
    const style = document.createElement('style');
    style.textContent = `
        .success-toast {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: rgba(34, 197, 94, 0.9);
            color: white;
            padding: 1rem 2rem;
            border-radius: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            animation: slideInRight 0.3s ease, fadeOut 0.3s ease 2.7s;
            backdrop-filter: blur(8px);
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(34, 197, 94, 0.2);
        }

        .invalid-prompt {
            background: linear-gradient(to right, #ef4444, #dc2626) !important;
            opacity: 0.7;
        }

        .invalid-prompt:hover {
            transform: none !important;
            box-shadow: none !important;
        }

        .ready-to-generate {
            background: linear-gradient(to right, #10b981, #059669) !important;
            animation: pulse-ready 2s infinite;
        }

        @keyframes pulse-ready {
            0%, 100% {
                box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
            }
            50% {
                box-shadow: 0 0 0 10px rgba(16, 185, 129, 0);
            }
        }

        @keyframes slideInRight {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        @keyframes fadeOut {
            from { opacity: 1; transform: translateY(0); }
            to { opacity: 0; transform: translateY(10px); }
        }

        .searching .fa-search {
            animation: pulse 1s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.2); }
            100% { transform: scale(1); }
        }

        .highlight-upload .upload-area {
            animation: highlightPulse 1s ease-in-out;
            border-color: #99FF66;
        }

        @keyframes highlightPulse {
            0% {
                transform: scale(1);
                box-shadow: 0 0 0 0 rgba(153, 255, 102, 0.4);
            }
            50% {
                transform: scale(1.02);
                box-shadow: 0 0 0 20px rgba(153, 255, 102, 0);
            }
            100% {
                transform: scale(1);
                box-shadow: 0 0 0 0 rgba(153, 255, 102, 0);
            }
        }

        .prompt-textarea:focus {
            border-color: #99FF66;
            box-shadow: 0 0 0 3px rgba(153, 255, 102, 0.1);
        }

        /* SweetAlert Customization */
        .swal2-popup {
            background: #1f2937 !important;
            color: #ffffff !important;
        }

        .swal2-title {
            color: #ffffff !important;
        }

        .swal2-content {
            color: #d1d5db !important;
        }

        .swal2-confirm {
            background: #99FF66 !important;
            color: #000000 !important;
        }

        .swal2-timer-progress-bar {
            background: #99FF66 !important;
        }
    `;
    document.head.appendChild(style);
});
 