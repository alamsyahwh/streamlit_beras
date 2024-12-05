import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from matplotlib.ticker import MaxNLocator, FuncFormatter
from babel.numbers import format_currency

sns.set(style='dark')

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://img.freepik.com/free-psd/fire-element-illustration_23-2150396733.jpg?t=st=1733216527~exp=1733220127~hmac=31c0586264a5bc9ad6aebc6fc08b03dcc484265442d4e751649734bcd37c3717&w=740")
    st.sidebar.header("Kelompok 5")
    st.sidebar.write("Alamsyah Wirayudha H")
    st.sidebar.write("Fajar Mulyana")
    st.sidebar.write("Rendi Firmansyah")
    st.sidebar.write("Ricky Pratama")

# Membaca data
df1 = pd.read_excel("luaspanen_2018-2020.xlsx", sheet_name="Sheet1")
df2 = pd.read_excel("luaspanen_2021-2023.xlsx", sheet_name="Sheet1")
df3 = pd.read_excel("harga_beras_2018-2023.xlsx", sheet_name="Sheet1")

# Preprocessing DataFrame 1
df1 = df1[3:]
df1.drop(df1.columns[1:7], axis=1, inplace=True)
df1.columns = ['provinsi', '2018', '2019', '2020']

# Preprocessing DataFrame 2
df2 = df2[3:]
df2.drop(df2.columns[1:7], axis=1, inplace=True)
df2.columns = ['provinsi', '2021', '2022', '2023']

# Preprocessing DataFrame 3
df3 = df3[3:]
df3.drop(df3.columns[1:13], axis=1, inplace=True)

# Menggabungkan df1 dan df2 berdasarkan kolom 'provinsi'
df_combined = pd.merge(df1, df2, on="provinsi")

# Mengubah kolom tahun menjadi numerik
for year in ['2018', '2019', '2020', '2021', '2022', '2023']:
    df_combined[year] = pd.to_numeric(df_combined[year], errors='coerce')

# Judul aplikasi
st.title("Data Produksi Beras Per Tahun")

# Dropdown untuk memilih tahun
tahun = st.selectbox("Pilih Tahun:", ['2018', '2019', '2020', '2021', '2022', '2023'])

# Filter data untuk menghapus baris "Indonesia"
data_tahun = df_combined[df_combined['provinsi'] != 'INDONESIA'][['provinsi', tahun]]

# Membuat bar chart
fig, ax = plt.subplots(figsize=(10, 6))

# Membuat bar chart berdasarkan Produksi Beras
bars = ax.bar(data_tahun['provinsi'], data_tahun[tahun], color='skyblue')
ax.set_title(f'Produksi Beras Tiap Provinsi di Tahun {tahun}', fontsize=16)
ax.set_xlabel('Provinsi', fontsize=12)
ax.set_ylabel('Produksi Beras', fontsize=12)

# Mengatur label provinsi agar vertikal
plt.xticks(rotation=90)

# Menampilkan grafik di Streamlit
st.pyplot(fig)

# Menambahkan nama kolom pada df3
df3.columns = ['Tahun', 'Harga']

# Menampilkan DataFrame
st.title("Data Harga Beras 2018 - 2023")

# Membuat line chart untuk harga beras
fig, ax = plt.subplots(figsize=(10, 6))

# Membuat line chart berdasarkan harga beras
ax.plot(df3['Tahun'], df3['Harga'], marker='s', color='orange', linestyle='-', linewidth=2, markersize=8)

# Menambahkan label dan judul
ax.set_title('Harga Beras Per Tahun', fontsize=16)
ax.set_xlabel('Tahun', fontsize=12)
ax.set_ylabel('Harga (IDR)', fontsize=12)

# Menampilkan grafik di Streamlit
st.pyplot(fig)

# Menampilkan Total Produksi Indonesia per Tahun
st.title("Total Produksi Beras Indonesia (2018-2023)")

# Ambil data produksi untuk Indonesia dari df1 dan df2
indonesia_produksi_df1 = df1[df1['provinsi'] == 'INDONESIA'].iloc[0, 1:]
indonesia_produksi_df2 = df2[df2['provinsi'] == 'INDONESIA'].iloc[0, 1:]

# Gabungkan produksi Indonesia dari df1 dan df2 untuk periode 2018-2023
total_produksi_indonesia = pd.concat([indonesia_produksi_df1, indonesia_produksi_df2])

# Membuat line chart untuk total produksi Indonesia
fig, ax = plt.subplots(figsize=(10, 6))

# Plot untuk total produksi Indonesia
ax.plot(total_produksi_indonesia.index, total_produksi_indonesia.values, marker='o', color='green', linestyle='-', linewidth=2, markersize=8)

# Menambahkan label dan judul
ax.set_title('Total Produksi Beras Indonesia (2018-2023)', fontsize=16)
ax.set_xlabel('Tahun', fontsize=12)
ax.set_ylabel('Produksi (ribu ton)', fontsize=12)

# Menampilkan grafik di Streamlit
st.pyplot(fig)

# --- Grafik Perbandingan Produksi dan Harga Beras (Dual-axis Line Chart) ---

st.title('Perbandingan Produksi dan Harga Beras di Indonesia (2018 - 2023)')
# Ambil data produksi untuk Indonesia dari df1 dan df2
produksi_indonesia = pd.concat([
    df1[df1['provinsi'] == 'INDONESIA'].iloc[0, 1:],  # Data produksi 2018-2020
    df2[df2['provinsi'] == 'INDONESIA'].iloc[0, 1:]   # Data produksi 2021-2023
])

years = df_combined.columns[1:]

# Membuat figure dan axis
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot untuk produksi beras (sumbu y pertama)
ax1.set_xlabel('Tahun')
ax1.set_ylabel('Produksi Beras (ribu ton)', color='blue')
ax1.plot(years, produksi_indonesia.values, marker='o', label='Produksi Beras', color='blue', linestyle='-', linewidth=3, markersize=8)
ax1.tick_params(axis='y', labelcolor='blue')

# Membuat sumbu y kedua untuk harga beras
ax2 = ax1.twinx()  # Inisialisasi sumbu y kedua yang berbagi sumbu x
ax2.set_ylabel('Harga Beras (IDR)', color='orange')
ax2.plot(years, df3['Harga'], marker='s', label='Harga Beras', color='orange', linestyle='-', linewidth=2, markersize=8)
ax2.tick_params(axis='y', labelcolor='orange')

# Menambahkan judul dan grid
plt.title('Perbandingan Produksi dan Harga Beras per Tahun')
fig.tight_layout()  # Agar layout tidak terpotong

# Menampilkan grid untuk sumbu x
ax1.grid(True)

# Menampilkan grafik di Streamlit
st.pyplot(fig)
