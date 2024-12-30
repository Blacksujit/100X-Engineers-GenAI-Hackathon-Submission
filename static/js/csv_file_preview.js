document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const noFileMessage = document.getElementById('noFileMessage');
    const csvPreview = document.getElementById('csvPreview');
    const previewHeader = document.getElementById('previewHeader');
    const previewBody = document.getElementById('previewBody');
    
    // Clear previous preview content
    previewHeader.innerHTML = '';
    previewBody.innerHTML = '';
    
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

                // Create table header from the first row of the CSV
                const headers = rows[0];
                headers.forEach(header => {
                    const th = document.createElement('th');
                    th.textContent = header;
                    previewHeader.appendChild(th);
                });

                // Create table rows from CSV data
                rows.slice(1).forEach(row => {
                    const tr = document.createElement('tr');
                    row.forEach(cell => {
                        const td = document.createElement('td');
                        td.textContent = cell;
                        tr.appendChild(td);
                    });
                    previewBody.appendChild(tr);
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
                    previewHeader.appendChild(th);
                });

                // Create table rows from XLSX data
                rows.slice(1).forEach(row => {
                    const tr = document.createElement('tr');
                    row.forEach(cell => {
                        const td = document.createElement('td');
                        td.textContent = cell;
                        tr.appendChild(td);
                    });
                    previewBody.appendChild(tr);
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
                    previewHeader.appendChild(th);
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
                    previewBody.appendChild(tr);
                });
            };
            reader.readAsText(file);
        }
        
        else {
            alert('Unsupported file type. Please upload CSV, XLSX, or TXT files.');
        }
    }
});
