import matplotlib.pyplot as plt
import pandas as pd

# Data SSIM vs Kompresi
data = {
    'Kompresi (%)': [90, 70, 50, 30, 10],
    'SSIM': [0.978, 0.952, 0.900, 0.812, 0.780]
}

df = pd.DataFrame(data)

# Hitung ΔSSIM dan dQ/dx
df['ΔSSIM'] = df['SSIM'].diff(-1)
df['Δx'] = df['Kompresi (%)'].diff(-1)
df['dQ/dx'] = (df['ΔSSIM'] / df['Δx']).abs()

# Hapus baris terakhir (karena tidak ada selisih)
df = df[:-1]

# Tampilkan tabel hasil
print("Tabel Laju Perubahan SSIM:")
print(df[['Kompresi (%)', 'ΔSSIM', 'Δx', 'dQ/dx']])

# Hitung total kehilangan kualitas (integral numerik sederhana)
total_loss = (df['dQ/dx'] * df['Δx']).sum()
print(f"\nTotal kehilangan kualitas (L): {total_loss:.3f} atau {total_loss*100:.1f}% dari citra asli")

# Plot grafik
plt.plot(data['Kompresi (%)'], data['SSIM'], marker='o', color='blue', linewidth=2)
plt.gca().invert_xaxis()  # biar 90 -> 10 urut dari kiri ke kanan
plt.title('Grafik SSIM terhadap Kualitas Kompresi')
plt.xlabel('Kualitas Kompresi (%)')
plt.ylabel('SSIM')
plt.grid(True)
plt.show()
