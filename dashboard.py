import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
df_day = pd.read_csv("day.csv")
df_hour = pd.read_csv("hour.csv")


# Konversi kolom tanggal
df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

# Sidebar
st.sidebar.title("Dashboard Peminjaman Sepeda")
data_option = st.sidebar.selectbox("Pilih Dataset:", ["Data Harian", "Data Per Jam"])

# Pilih dataset
df = df_day if data_option == "Data Harian" else df_hour

# Filter Tanggal
start_date = pd.to_datetime(st.sidebar.date_input("Tanggal Awal", df['dteday'].min()))
end_date = pd.to_datetime(st.sidebar.date_input("Tanggal Akhir", df['dteday'].max()))
df_filtered = df[(df['dteday'] >= start_date) & (df['dteday'] <= end_date)]

# Metrik Utama
total_peminjaman = df_filtered['cnt'].sum()
rata_rata_peminjaman = df_filtered['cnt'].mean()
pertumbuhan = ((df_filtered['cnt'].iloc[-1] - df_filtered['cnt'].iloc[0]) / df_filtered['cnt'].iloc[0]) * 100 if len(df_filtered) > 1 else 0

st.title("📊 Dashboard Peminjaman Sepeda 🚴‍♂️")
col1, col2, col3 = st.columns(3)
col1.metric("Total Peminjaman", f"{total_peminjaman:,.0f}")
col2.metric("Rata-rata / Hari", f"{rata_rata_peminjaman:,.0f}")
col3.metric("Pertumbuhan", f"{pertumbuhan:.2f}%")

# Visualisasi Tren Peminjaman
st.write("## Tren Peminjaman Sepeda")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x=df_filtered['dteday'], y=df_filtered['cnt'], ax=ax, color='green')
ax.set_title("Tren Peminjaman Sepeda")
plt.xticks(rotation=45)
st.pyplot(fig)

# Distribusi Peminjaman
st.write("## Distribusi Peminjaman Sepeda")
fig2, ax2 = plt.subplots(figsize=(12, 6))
sns.histplot(df_filtered['cnt'], kde=True, color='blue', ax=ax2)
st.pyplot(fig2)

# Perbandingan Weekday vs Weekend
df_filtered['weekday'] = df_filtered['dteday'].dt.dayofweek
df_filtered['is_weekend'] = df_filtered['weekday'].apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')

st.write("## Perbandingan Peminjaman Weekday vs Weekend")
fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.boxplot(x="is_weekend", y="cnt", data=df_filtered, ax=ax3, palette=["blue", "orange"])
st.pyplot(fig3)

st.write("**Dashboard ini dirancang untuk memberikan wawasan lebih dalam terhadap pola peminjaman sepeda.** 🚴")
