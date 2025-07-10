const fileInput = document.getElementById('file-upload');
const fileLabel = document.getElementById('file-upload-label');
const fileNameDisplay = document.getElementById('file-name');

// نمایش نام فایل بعد از انتخاب
fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        fileNameDisplay.textContent = `فایل انتخاب شده: ${fileInput.files[0].name}`;
    } else {
        fileNameDisplay.textContent = '';
    }
});

// فعال کردن درگ و دراپ روی label
fileLabel.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileLabel.classList.add('dragover');
});

fileLabel.addEventListener('dragleave', (e) => {
    e.preventDefault();
    fileLabel.classList.remove('dragover');
});

fileLabel.addEventListener('drop', (e) => {
    e.preventDefault();
    fileLabel.classList.remove('dragover');

    if (e.dataTransfer.files.length > 0) {
        fileInput.files = e.dataTransfer.files;
        fileNameDisplay.textContent = `فایل انتخاب شده: ${fileInput.files[0].name}`;
    }
});
