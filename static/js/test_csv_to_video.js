        // DOM Elements
const uploadContainer = document.getElementById('upload-container');
const fileInput = document.getElementById('file-input');
const previewContainer = document.getElementById('preview-container');
const tableHeader = document.getElementById('table-header');
const tableBody = document.getElementById('table-body');
const generateButton = document.getElementById('generate-button');
const videoContainer = document.getElementById('video-container');
const videoPlayer = document.getElementById('video-player');
const alertElement = document.getElementById('alert');
const loadingElement = document.getElementById('loading');
const searchInput = document.getElementById('table-search');
const rowCountElement = document.getElementById('row-count');
const columnCountElement = document.getElementById('column-count');
const downloadCsvBtn = document.getElementById('download-csv');
const downloadVideoBtn = document.getElementById('download-video');
const progressBar = document.querySelector('.progress-bar-fill');
const progressText = document.querySelector('.progress-text');

// State management
let currentData = [];
let filteredData = [];
    
        const allowedExtensions = ['csv', 'xlsx', 'xls', 'txt'];
        const maxSize = 10 * 1024 * 1024; // 10MB
    
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
    
        function showError(message) {
            alertElement.textContent = message;
            alertElement.style.display = 'block';
            setTimeout(() => {
                alertElement.style.display = 'none';
            }, 5000);
        }
    
        function showLoading(show) {
            loadingElement.style.display = show ? 'block' : 'none';
        }

        function updateLoadingPhases() {
            const phases = document.querySelectorAll('.phase');
            let currentPhase = 0;
            
            function activateNextPhase() {
                if (currentPhase > 0) {
                    phases[currentPhase - 1].classList.remove('active');
                }
                if (currentPhase < phases.length) {
                    phases[currentPhase].classList.add('active');
                    currentPhase++;
                    setTimeout(activateNextPhase, 2000); // Switch phase every 2 seconds
                }
            }
            
            activateNextPhase();
        }

        function resetLoadingPhases() {
            const phases = document.querySelectorAll('.phase');
            phases.forEach(phase => phase.classList.remove('active'));
            phases[0].classList.add('active');
        }

        function updateLoadingStatus(message) {
            const statusElement = document.querySelector('.loading-status');
            if (statusElement) {
                statusElement.textContent = message;
            }
        }
    
        async function handleFile(file) {
    try {
        progressBar.style.width = '0%';
        alertElement.style.display = 'none';
        updateProgress(0);

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

        updateProgress(20);

        let data;
        if (fileExtension === 'csv' || fileExtension === 'txt') {
            data = await parseCSV(file);
        } else {
            data = await parseExcel(file);
        }

        updateProgress(60);

        // Store the full dataset
        currentData = data;
        filteredData = [...data];

        // Enable download CSV button
        downloadCsvBtn.disabled = false;

        displayPreview(data);
        previewContainer.style.display = 'block';
        previewContainer.classList.add('active');

        updateProgress(100);

        // Show success message
        showSuccess('File loaded successfully!');

    } catch (error) {
        showError(error.message);
        updateProgress(0);
    } finally {
        setTimeout(() => {
            showLoading(false);
        }, 500);
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
        showError('No data to display');
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
    progressBar.style.width = `${percent}%`;
    progressText.textContent = `${Math.round(percent)}%`;

    if (percent === 100) {
        progressBar.classList.add('complete');
        setTimeout(() => progressBar.classList.remove('complete'), 1000);
    }
}

function showSuccess(message) {
    const alert = document.createElement('div');
    alert.className = 'success-toast';
    alert.innerHTML = `
        <i class="fas fa-check-circle"></i>
        <span>${message}</span>
    `;
    document.body.appendChild(alert);
    setTimeout(() => alert.remove(), 3000);
}

// Generate Video with Progress
generateButton.addEventListener('click', async () => {
    try {
        generateButton.disabled = true;
        generateButton.classList.add('loading');
        showLoading(true); // Now this will show the creative loader in the correct position
        updateProgress(0);

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        // Simulate progress updates (replace with real progress when available)
        const progressInterval = setInterval(() => {
            const currentWidth = parseInt(progressBar.style.width) || 0;
            if (currentWidth < 90) {
                updateProgress(currentWidth + Math.random() * 10);
            }
        }, 500);

        const response = await fetch('/generate_video_from_csv', {
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
        
        videoPlayer.src = responseData.video_path;
        videoContainer.style.display = 'block';
        videoContainer.classList.add('active');

        // Enable download video button
        downloadVideoBtn.disabled = false;
        showSuccess('Video generated successfully!');

    } catch (error) {
        showError(error.message);
        updateProgress(0);
    } finally {
        generateButton.disabled = false;
        generateButton.classList.remove('loading');
        showLoading(false);
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
    ].join('\\n');

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

// Reset page state function
function resetPageState() {
    // Reset file input
    fileInput.value = '';
    
    // Reset data states
    currentData = [];
    filteredData = [];
    
    // Clear table
    tableHeader.innerHTML = '';
    tableBody.innerHTML = '';
    
    // Reset search
    if (searchInput) {
        searchInput.value = '';
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
    
    // Reset buttons
    generateButton.disabled = false;
    generateButton.classList.remove('loading');
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
        showSuccess('Ready for new video generation!');
    }, 500);
});

// Make table container resizable
const resizeHandle = document.querySelector('.resize-handle');
let isResizing = false;
let startY;
let startHeight;

resizeHandle.addEventListener('mousedown', (e) => {
    isResizing = true;
    startY = e.clientY;
    startHeight = document.querySelector('.table-container').offsetHeight;
    document.body.style.cursor = 'row-resize';
});

document.addEventListener('mousemove', (e) => {
    if (!isResizing) return;
    
    const delta = e.clientY - startY;
    const newHeight = startHeight + delta;
    const container = document.querySelector('.table-container');
    
    if (newHeight >= 200 && newHeight <= window.innerHeight * 0.8) {
        container.style.height = `${newHeight}px`;
    }
});

document.addEventListener('mouseup', () => {
    isResizing = false;
    document.body.style.cursor = '';
});

// Success toast styling
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
`;
document.head.appendChild(style);
        