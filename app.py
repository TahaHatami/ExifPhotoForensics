from flask import Flask, request, render_template, send_file
import subprocess
import os
import csv
import uuid

app = Flask(__name__)

# مسیر exiftool.exe
EXIFTOOL_PATH = os.path.join(os.path.dirname(__file__), 'exiftool.exe')

# پوشه‌های ذخیره‌سازی
UPLOAD_FOLDER = os.path.join('static', 'uploads')
TEMP_FOLDER = os.path.join('static', 'temp')

# ساخت پوشه‌ها در صورت عدم وجود
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)

def extract_exif_with_exiftool(file_path):
    try:
        command = [EXIFTOOL_PATH, file_path]
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            return f"خطا در اجرای ExifTool: {result.stderr}"

        output = result.stdout
        # حذف خط مربوط به نسخه ExifTool
        output = "\n".join([line for line in output.split("\n") if not line.startswith("ExifTool Version Number")])
        return output
    except Exception as e:
        return f"خطا در استخراج متادیتا: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image_file = request.files['image']

        if image_file:
            filename = f"{uuid.uuid4().hex}_{image_file.filename}"
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            image_file.save(save_path)

            url_path = save_path.replace('\\', '/')

            metadata = extract_exif_with_exiftool(save_path)

            # مطمئن شدن از وجود پوشه temp قبل از نوشتن فایل‌ها
            os.makedirs(TEMP_FOLDER, exist_ok=True)

            # ساخت فایل .txt
            txt_path = os.path.join(TEMP_FOLDER, f"{filename}.txt")
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(metadata)

            # ساخت فایل .csv
            csv_path = os.path.join(TEMP_FOLDER, f"{filename}.csv")
            with open(csv_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                for line in metadata.splitlines():
                    if ':' in line:
                        key, value = line.split(':', 1)
                        writer.writerow([key.strip(), value.strip()])

            return render_template(
                'index.html',
                metadata=metadata,
                image_path=url_path,
                txt_filename=f"{filename}",
            )

    return render_template('index.html', metadata=None)

@app.route('/download/<filetype>/<filename>')
def download_file(filetype, filename):
    if filetype not in ['txt', 'csv']:
        return "فرمت پشتیبانی نمی‌شود", 400

    file_path = os.path.join(TEMP_FOLDER, f"{filename}.{filetype}")
    if not os.path.exists(file_path):
        return "فایل پیدا نشد", 404

    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
