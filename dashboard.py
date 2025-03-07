import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Baca file CSV dengan path lengkap
df_day = pd.read_csv("C:/Users/testo/Documents/Bike-sharing-dataset/day.csv")
df_hour = pd.read_csv("C:/Users/testo/Documents/Bike-sharing-dataset/hour.csv")

# Pastikan 'dteday' diubah menjadi tipe datetime
df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

# Sidebar
st.sidebar.title("Dashboard Peminjaman Sepeda")
data_option = st.sidebar.selectbox("Pilih Dataset:", ["Data Harian", "Data Per Jam"])

# Menampilkan dataset yang dipilih
st.title("📊 Analisis Peminjaman Sepeda 🚴‍♂️")
if data_option == "Data Harian":
    st.write("### 5 Data Pertama dari Dataset Harian")
    st.write(df_day.head())
    df = df_day
else:
    st.write("### 5 Data Pertama dari Dataset Per Jam")
    st.write(df_hour.head())
    df = df_hour

# Menambahkan filter dan analisis lebih lanjut
st.sidebar.write("### Filter Data")
start_date = st.sidebar.date_input("Pilih Tanggal Awal", pd.to_datetime(df['dteday'].min()))
end_date = st.sidebar.date_input("Pilih Tanggal Akhir", pd.to_datetime(df['dteday'].max()))

# Filter data berdasarkan tanggal
df_filtered = df[(df['dteday'] >= pd.to_datetime(start_date)) & (df['dteday'] <= pd.to_datetime(end_date))]

# Visualisasi Tren Peminjaman Sepeda
st.write(f"## Tren Peminjaman Sepeda dari {start_date} sampai {end_date}")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x=pd.to_datetime(df_filtered['dteday']), y=df_filtered['cnt'], ax=ax, color='green')
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Peminjaman Sepeda")
ax.set_title(f"Tren Peminjaman Sepeda {start_date} - {end_date}")
ax.grid(True)
plt.xticks(rotation=45)
st.pyplot(fig)

# Menambahkan analisis distribusi
st.write("## Analisis Distribusi Peminjaman Sepeda")
fig2, ax2 = plt.subplots(figsize=(12, 6))
sns.histplot(df_filtered['cnt'], kde=True, color='blue', ax=ax2)
ax2.set_xlabel("Jumlah Peminjaman Sepeda")
ax2.set_ylabel("Frekuensi")
ax2.set_title("Distribusi Peminjaman Sepeda")
st.pyplot(fig2)

# Penutup
st.write("""
    **Dashboard ini dibuat dengan Streamlit untuk eksplorasi dataset peminjaman sepeda.**
    Dengan visualisasi interaktif dan analisis yang lebih mendalam, Anda bisa menggali lebih banyak informasi tentang tren penggunaan sepeda di berbagai periode.
""")
