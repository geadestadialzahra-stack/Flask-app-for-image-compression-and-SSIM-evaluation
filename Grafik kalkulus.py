import pandas as pd
import matplotlib.pyplot as plt

# Data dari tabel
data = {
    "Kualitas (%)": [90, 70, 50, 30, 10],
    "Ukuran File (KB)": [1725.57, 896.29, 633.28, 451.65, 182.81],
    "SSIM": [0.9820, 0.9538, 0.9367, 0.9128, 0.8179],
    "PSNR": [40.50, 35.87, 34.27, 32.63, 28.47]
}

# Membuat DataFrame
df = pd.DataFrame(data)

# Urutkan agar sumbu X naik dari 10 → 90
df = df.sort_values(by="Kualitas (%)")

# Membuat grafik hubungan tingkat kompresi terhadap SSIM
plt.figure(figsize=(8, 5))
plt.plot(df["Kualitas (%)"], df["SSIM"], marker='o', color='blue')

# Menampilkan nilai SSIM di atas tiap titik
for x, y in zip(df["Kualitas (%)"], df["SSIM"]):
    plt.text(x, y + 0.002, f"{y:.4f}", ha='center', fontsize=9)

# Memberi judul dan label sumbu
plt.title("Hubungan Tingkat Kompresi terhadap SSIM", fontsize=14)
plt.xlabel("Kualitas Kompresi (%)", fontsize=12)
plt.ylabel("Nilai SSIM", fontsize=12)
plt.ylim(0.80, 1.00)  # batas sumbu Y biar sesuai dengan data
plt.grid(True)

# Menampilkan grafik
plt.show()
