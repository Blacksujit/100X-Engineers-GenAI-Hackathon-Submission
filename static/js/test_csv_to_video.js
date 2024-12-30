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
    
        async function handleFile(file) {
            try {
                showLoading(true);
                alertElement.style.display = 'none';
        
                if (!file) return;
        
                if (file.size > maxSize) {
                    throw new Error('File size too large. Please upload a file smaller than 10MB.');
                }
        
                const fileExtension = file.name.split('.').pop().toLowerCase();
        
                if (!allowedExtensions.includes(fileExtension)) {
                    showError(`Invalid file type. Only ${allowedExtensions.join(', ')} files are allowed. You uploaded a .${fileExtension} file.`);
                    return;
                }
        
                let data;
                if (fileExtension === 'csv' || fileExtension === 'txt') {
                    data = await parseCSV(file);
                } else {
                    data = await parseExcel(file);
                }
        
                displayPreview(data.slice(0, 100));
                previewContainer.style.display = 'block';
        
            } catch (error) {
                showError(error.message);
            } finally {
                showLoading(false);
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
    
        function displayPreview(data) {
            if (!data.length) return;
    
            tableHeader.innerHTML = '';
            tableBody.innerHTML = '';
    
            Object.keys(data[0]).forEach(header => {
                const th = document.createElement('th');
                th.textContent = header;
                tableHeader.appendChild(th);
            });
    
            data.forEach(row => {
                const tr = document.createElement('tr');
                Object.values(row).forEach(cell => {
                    const td = document.createElement('td');
                    td.textContent = cell;
                    tr.appendChild(td);
                });
                tableBody.appendChild(tr);
            });
        }
    
        generateButton.addEventListener('click', async () => {
            try {
                generateButton.disabled = true;
                generateButton.textContent = 'Generating Video...';
                showLoading(true);
        
                const formData = new FormData();
                formData.append('file', fileInput.files[0]);
        
                const response = await fetch('/generate_video_from_csv', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'Accept': 'application/json',
                    },
                    credentials: 'include',
                });
        
                if (!response.ok) {
                    const text = await response.text();
                    throw new Error('Error generating video: ' + text);
                }
        
                const responseData = await response.json();
        
                if (responseData.error) {
                    throw new Error(responseData.error);
                }
        
                videoPlayer.src = responseData.video_path;
                videoContainer.style.display = 'block';
        
            } catch (error) {
                showError(error.message);
            } finally {
                generateButton.disabled = false;
                generateButton.textContent = 'Generate Video';
                showLoading(false);
            }
        });



        // progress bar update code 
        
        // function updateProgress(percent) {
        //     const progressBar = document.querySelector('.progress');
        //     progressBar.style.width = `${percent}%`;
        // }

        
        // document.getElementById('download-btn').addEventListener('click', () => {
        //     const videoPath = document.getElementById('video-player').src;
        //     const anchor = document.createElement('a');
        //     anchor.href = videoPath;
        //     anchor.download = 'generated_video.mp4';
        //     document.body.appendChild(anchor);
        //     anchor.click();
        //     document.body.removeChild(anchor);
        // });
        