document.addEventListener('DOMContentLoaded', () => {
    const generateButton = document.getElementById('generateButton');
    const progressBar = document.getElementById('progress');
    const resultContainer = document.getElementById('resultContainer');
    const resultVideo = document.getElementById('resultVideo');
    const errorContainer = document.getElementById('errorContainer');
    const downloadBtn = document.getElementById('downloadBtn');
    const videoSection = document.getElementById('videoSection');
    const regenerateBtn = document.getElementById('regenerateBtn');
    const textInput = document.getElementById('textInput');
    const progressBarContainer = document.querySelector('.progress-bar');
    let isGenerating = false;

    // Ensure we don't bind multiple times if this script is reloaded
    generateButton?.removeEventListener('click', noop);

    generateButton.addEventListener('click', async () => {
        if (isGenerating) return;
        const inputText = textInput.value.trim();
        if (!inputText) {
            textInput.classList.add('error');
            showNotification('Please enter some text to generate a video', 'error');
            setTimeout(() => textInput.classList.remove('error'), 1200);
            return;
        }

        isGenerating = true;
        generateButton.classList.add('loading');
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

            let data;
            try {
                data = await response.json();
            } catch (e) {
                throw new Error('Unexpected server response');
            }

            if (!response.ok) {
                throw new Error(data.error || 'Failed to generate video');
            }

            resultVideo.src = data.video_path + `?t=${new Date().getTime()}`;
            resultVideo.style.display = 'block';
            resultContainer.classList.add('active');
            videoSection?.classList.add('active');
            downloadBtn.onclick = () => {
                const link = document.createElement('a');
                link.href = data.video_path;
                link.download = 'video.mp4';
                link.click();
            };
            showNotification('Video generated successfully!', 'success');

        } catch (error) {
            showNotification(error.message || 'An error occurred while generating the video', 'error');
        } finally {
            hideLoading();
            generateButton.disabled = false;
            generateButton.classList.remove('loading');
            isGenerating = false;
        }
    });

    function showNotification(message, type = 'info', ms = 2500) {
        // Prefer SweetAlert2 if present
        if (window.Swal) {
            const icon = type === 'success' ? 'success' : type === 'error' ? 'error' : 'info';
            Swal.fire({
                toast: true,
                position: 'center-end',
                icon,
                title: message,
                showConfirmButton: false,
                timer: ms,
                timerProgressBar: true,
                iconColor: icon === 'success' ? '#16a34a' : icon === 'error' ? '#ef4444' : '#06b6d4',
                customClass: {
                    container: 'notif-container-offset',
                    popup: `swal2-bubble swal2-${icon}`
                },
                didOpen: (toast) => {
                    toast.addEventListener('mouseenter', Swal.stopTimer)
                    toast.addEventListener('mouseleave', Swal.resumeTimer)
                }
            });
            return;
        }
        // Fallback to custom notification box
        errorContainer.innerText = message;
        errorContainer.classList.remove('success', 'error', 'info');
        errorContainer.classList.add('show', type);
        setTimeout(() => {
            errorContainer.classList.remove('show', 'success', 'error', 'info');
        }, ms);
    }

    function showLoading() {
        progressBar.style.width = '35%';
    }

    function hideLoading() {
        progressBar.style.width = '100%';
        setTimeout(() => {
            progressBarContainer.style.display = 'none';
            progressBar.style.width = '0%';
        }, 500);
    }

    // Regenerate flow: clears fields and prompts user
    regenerateBtn?.addEventListener('click', () => {
        regenerateBtn.classList.add('loading');
        // clear inputs and outputs
        textInput.value = '';
        resultVideo.removeAttribute('src');
        resultContainer.classList.remove('active');
        videoSection?.classList.remove('active');
        // focus back on input
        textInput.focus();
        // update char count if present
        const cc = document.getElementById('charCount');
        if (cc) cc.textContent = '0';
        setTimeout(() => {
            regenerateBtn.classList.remove('loading');
            showNotification('everything is cleared. Enter a new prompt to generate a video.', 'info', 3000);
        }, 400);
    });
    function noop(){}
});

document.addEventListener('DOMContentLoaded', function() {
	const textarea = document.getElementById('textInput');
	const charCount = document.getElementById('charCount');
	const chips = document.querySelectorAll('.prompt-chip');
	const genBtn = document.getElementById('generateButton');

	function updateCount() {
		if (!textarea || !charCount) return;
		charCount.textContent = textarea.value.length;
	}

	if (textarea) {
		textarea.addEventListener('input', updateCount);
		updateCount();
	}

	chips.forEach(chip => {
		chip.addEventListener('click', () => {
			const sample = chip.getAttribute('data-sample') || '';
			if (textarea) {
				textarea.value = sample;
				textarea.focus();
				updateCount();
			}
		});
	});

	// Loading state is handled in static/js/text_to_video.js after validation
});
