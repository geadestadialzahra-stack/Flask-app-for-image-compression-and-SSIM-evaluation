import cv2
import numpy as np
import math

# === 1. Baca gambar asli dan hasil kompresi ===
img_asli = cv2.imread("#GambarAsli500kb_11zon.jpg")        # pakai format JPG
img_kompres = cv2.imread("#GambarKompres 70%.jpg")  # hasil kompresinya juga JPG

# === 2. Cek apakah ukuran gambar sama ===
if img_asli.shape != img_kompres.shape:
    print("⚠️ Ukuran gambar berbeda! Harus diresize dulu biar sama.")
    img_kompres = cv2.resize(img_kompres, (img_asli.shape[1], img_asli.shape[0]))

# === 3. Hitung selisih piksel (absolut) ===
selisih = cv2.absdiff(img_asli, img_kompres)
print("Rata-rata selisih piksel (B, G, R):", np.mean(selisih, axis=(0,1)))

# === 4. Hitung Mean Squared Error (MSE) ===
mse = np.mean((img_asli - img_kompres) ** 2)
print("Nilai MSE =", mse)

# === 5. Hitung Peak Signal-to-Noise Ratio (PSNR) ===
if mse == 0:
    psnr = 100  # kalau gambar identik
else:
    psnr = 10 * math.log10((255 ** 2) / mse)

print("Nilai PSNR =", psnr, "dB")

# === 6. (Opsional) Simpan hasil perbedaan antar piksel ===
cv2.imwrite("selisih.jpg", selisih)
print("Gambar selisih disimpan sebagai 'selisih.jpg'")

