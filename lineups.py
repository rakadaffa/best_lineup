import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. Memuat Data dari File CSV
PathFile = r"D:\\Algeo\\Makalah\\Cavs_Stats.csv"
KerangkaData = pd.read_csv(PathFile)

# Ambil nama pemain dan statistik
NamaPemain = KerangkaData["Player"].values
Statistik = KerangkaData.columns[1:]

# Filter data
RataRataMenit = KerangkaData["Min"].mean()
KerangkaDataTersaring = KerangkaData[KerangkaData["Min"] > RataRataMenit]

# Kolom yang digunakan untuk matriks
KolomDipilih = ["PTS", "REB", "AST", "STL", "BLK", "FG%"]
NamaPemain = KerangkaDataTersaring["Player"].values
Statistik = KolomDipilih
DataTersaring = KerangkaDataTersaring[KolomDipilih].values

# Normalisasi Min-Max
DataMin = np.min(DataTersaring, axis=0)
DataMax = np.max(DataTersaring, axis=0)
DataNormalisasi = pd.DataFrame(
    (DataTersaring - DataMin) / (DataMax - DataMin),
    columns=KolomDipilih,
    index=NamaPemain
)

# Tambahkan kolom posisi pemain dan kode huruf
PosisiPemain = {
    "Donovan Mitchell": "A",
    "Darius Garland": "B",
    "Evan Mobley": "C",
    "Jarrett Allen": "D",
    "Caris LeVert": "E",
    "Georges Niang": "F",
    "Sam Merrill": "G",
    "Isaac Okoro": "H",
    "Dean Wade": "I"
}

KerangkaData["Position"] = KerangkaData["Player"].map(PosisiPemain)

# Filter data berdasarkan posisi
Guards = KerangkaData[KerangkaData["Position"].isin(["A", "B", "E", "G"])]
Forwards = KerangkaData[KerangkaData["Position"].isin(["C", "F", "H"])]
Centers = KerangkaData[KerangkaData["Position"].isin(["D", "I"])]

# # Validasi jumlah pemain per posisi
# if len(Guards) < 2 or len(Forwards) < 2 or len(Centers) < 1:
#     raise ValueError("Tidak cukup pemain untuk setiap posisi dalam line-up")

# Fungsi untuk menghasilkan kombinasi
def Kombinasi(arr, r):
    def KombinasiRekursif(mulai, jalur):
        if len(jalur) == r:
            hasil.append(jalur)
            return
        for i in range(mulai, len(arr)):
            KombinasiRekursif(i + 1, jalur + [arr[i]])

    hasil = []
    KombinasiRekursif(0, [])
    return hasil

# Dapatkan semua kombinasi line-up
KombinasiGuards = Kombinasi(Guards["Position"].values, 2)
KombinasiForwards = Kombinasi(Forwards["Position"].values, 2)
KombinasiCenters = Kombinasi(Centers["Position"].values, 1)

# Gabungkan semua kombinasi
SemuaKombinasi = [
    kombinasi_guards + kombinasi_forwards + kombinasi_centers
    for kombinasi_guards in KombinasiGuards
    for kombinasi_forwards in KombinasiForwards
    for kombinasi_centers in KombinasiCenters
]

# Peta posisi ke nama pemain
PosisiKeNama = {v: k for k, v in PosisiPemain.items()}

# Fungsi menghitung bobot antar pemain berdasarkan data normalisasi
def HitungBobotNormalisasi(posisi1, posisi2, kolom_terpilih, data_normalisasi):
    pemain1 = PosisiKeNama[posisi1]
    pemain2 = PosisiKeNama[posisi2]
    statistik1 = data_normalisasi.loc[pemain1, kolom_terpilih]
    statistik2 = data_normalisasi.loc[pemain2, kolom_terpilih]
    bobot = (statistik1 + statistik2) / 2
    return bobot.sum()

# Hitung total bobot untuk setiap line-up
BobotLineupMenyerang = []
BobotLineupBertahan = []

for lineup in SemuaKombinasi:
    TotalBobotMenyerang = 0
    TotalBobotBertahan = 0
    for i in range(len(lineup)):
        for j in range(i + 1, len(lineup)):
            TotalBobotMenyerang += HitungBobotNormalisasi(
                lineup[i], lineup[j], ["PTS", "AST", "FG%"], DataNormalisasi
            )
            TotalBobotBertahan += HitungBobotNormalisasi(
                lineup[i], lineup[j], ["REB", "BLK", "STL"], DataNormalisasi
            )
    BobotLineupMenyerang.append(TotalBobotMenyerang)
    BobotLineupBertahan.append(TotalBobotBertahan)

# Label untuk setiap line-up
LabelLineup = [''.join(lineup) for lineup in SemuaKombinasi]

# Gabungkan lineup dengan bobot
DataBobotMenyerang = pd.DataFrame({'LineUp': LabelLineup, 'Bobot': BobotLineupMenyerang})
DataBobotMenyerang = DataBobotMenyerang.sort_values(by='Bobot', ascending=False)

# Plot grafik batang horizontal
plt.figure(figsize=(10, len(DataBobotMenyerang) / 2))
plt.barh(DataBobotMenyerang['LineUp'], DataBobotMenyerang['Bobot'], color='blue', alpha=0.7, label='PTS, AST, FG%')
plt.xlabel("Total Bobot")
plt.ylabel("Line-up")
plt.title("Perbandingan Total Bobot Line-up Fase Menyerang")
plt.gca().invert_yaxis()
plt.legend()
plt.tight_layout()
plt.show()

# Gabungkan lineup dengan bobot
DataBobotBertahan = pd.DataFrame({'LineUp': LabelLineup, 'Bobot': BobotLineupBertahan})
DataBobotBertahan = DataBobotBertahan.sort_values(by='Bobot', ascending=False)

# Plot grafik batang horizontal
plt.figure(figsize=(10, len(DataBobotBertahan) / 2))
plt.barh(DataBobotBertahan['LineUp'], DataBobotBertahan['Bobot'], color='green', alpha=0.7, label='REB, BLK, STL')
plt.xlabel("Total Bobot")
plt.ylabel("Line-up")
plt.title("Perbandingan Total Bobot Line-up Fase Bertahan")
plt.gca().invert_yaxis()
plt.legend()
plt.tight_layout()
plt.show()
