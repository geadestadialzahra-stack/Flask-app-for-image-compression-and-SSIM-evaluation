from flask import Flask, render_template, request, send_file
from PIL import Image
import os
import cv2
import numpy as np
from skimage.metrics import peak_signal_noise_ratio, structural_similarity

app = Flask(__name__)

# Folder penyimpanan
UPLOAD_FOLDER = 'static/uploads'
COMPRESSED_FOLDER = 'static/compressed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

# Kompresi gambar dengan konversi mode
def compress_image(input_path, output_path, quality_percent):
    img = Image.open(input_path)

    # Konversi ke RGB jika gambar punya transparansi
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')

    img.save(output_path, format='JPEG', quality=quality_percent, optimize=True)

# Hitung PSNR dan SSIM dengan validasi ukuran
def calculate_metrics(original_path, compressed_path):
    original = cv2.imread(original_path)
    compressed = cv2.imread(compressed_path)

    # Validasi ukuran minimum
    if original.shape[0] < 70 or original.shape[1] < 70:
        raise ValueError("Ukuran gambar terlalu kecil untuk analisis SSIM/PSNR.")

    psnr = peak_signal_noise_ratio(original, compressed)
    ssim = structural_similarity(original, compressed, channel_axis=2)
    return psnr, ssim

# Hitung ukuran file dan penghematan
def calculate_savings(original_path, compressed_path):
    original_size = os.path.getsize(original_path) / 1024  # KB
    compressed_size = os.path.getsize(compressed_path) / 1024  # KB
    savings = ((original_size - compressed_size) / original_size) * 100
    return round(original_size, 2), round(compressed_size, 2), round(savings, 2)

# Halaman utama
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['image']
        quality = int(request.form['quality'])

        filename = file.filename
        original_path = os.path.join(UPLOAD_FOLDER, filename)
        compressed_path = os.path.join(COMPRESSED_FOLDER, filename)

        file.save(original_path)
        compress_image(original_path, compressed_path, quality)

        try:
            psnr, ssim = calculate_metrics(original_path, compressed_path)
        except ValueError as e:
            psnr, ssim = 0, 0  # Atau bisa tampilkan pesan error di HTML

        ori_size, comp_size, savings = calculate_savings(original_path, compressed_path)

        return render_template('index.html',
                               original=filename,
                               psnr=psnr,
                               ssim=ssim,
                               ori_size=ori_size,
                               comp_size=comp_size,
                               savings=savings)
    return render_template('index.html')

# Endpoint download
@app.route('/download/<filename>')
def download(filename):
    path = os.path.join(COMPRESSED_FOLDER, filename)
    return send_file(path, as_attachment=True)

# Jalankan Flask
if __name__ == '__main__':
    app.run(debug=True)