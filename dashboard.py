import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df_day = pd.read_csv("day.csv")
df_hour = pd.read_csv("hour.csv")

# Konversi kolom tanggal
df_day["dteday"] = pd.to_datetime(df_day["dteday"])
df_hour["dteday"] = pd.to_datetime(df_hour["dteday"])

# Mapping nama musim
season_mapping = {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
df_day["season_name"] = df_day["season"].map(season_mapping)

# Sidebar untuk interaktif
st.sidebar.header("Filter Data")
selected_season = st.sidebar.selectbox(
    "Pilih Musim",
    df_day["season"].unique(),
    format_func=lambda x: season_mapping[x]
)
time_range = st.sidebar.slider("Pilih Rentang Jam", 0, 23, (6, 18))

# Filter data
df_day_filtered = df_day[df_day["season"] == selected_season]
df_hour_filtered = df_hour[
    (df_hour["season"] == selected_season) & 
    (df_hour["hr"].between(time_range[0], time_range[1]))
]

# Menampilkan header
st.header("📊 Dashboard Penyewaan Sepeda 🚲")

# Visualisasi 1: Perbandingan Penyewaan Antar Musim (Semua Data)
st.subheader("Perbandingan Penyewaan Antar Musim")
season_counts = df_day.groupby("season_name")["cnt"].sum().reset_index()

# Membuat warna berbeda untuk musim yang dipilih
colors = ["#FF9999" if season == season_mapping[selected_season] else "#66B2FF" for season in season_counts["season_name"]]

fig1, ax1 = plt.subplots()
ax1.bar(season_counts["season_name"], season_counts["cnt"], color=colors)
ax1.set_title("Total Penyewaan Sepeda per Musim")
ax1.set_xlabel("Musim")
ax1.set_ylabel("Total Penyewaan")
st.pyplot(fig1)

# Visualisasi 2: Tren Harian dalam Musim Terpilih
st.subheader(f"Tren Harian di {season_mapping[selected_season]}")
fig2, ax2 = plt.subplots(figsize=(10, 4))
sns.lineplot(
    data=df_day_filtered,
    x="dteday", 
    y="cnt",
    marker="o",
    color="#2CA02C"
)
ax2.set_title("Fluktuasi Harian Penyewaan Sepeda")
ax2.set_xlabel("Tanggal")
ax2.set_ylabel("Jumlah Penyewaan")
plt.xticks(rotation=45)
st.pyplot(fig2)

# Visualisasi 3: Pola Jam Penyewaan (Filter Musim + Jam)
st.subheader("Pola Penyewaan per Jam")
hourly_counts = df_hour_filtered.groupby("hr")["cnt"].mean().reset_index()

fig3, ax3 = plt.subplots()
sns.barplot(
    x="hr", 
    y="cnt", 
    data=hourly_counts,
    palette="viridis",
    ax=ax3
)
ax3.set_title("Rata-rata Penyewaan per Jam")
ax3.set_xlabel("Jam dalam Sehari")
ax3.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig3)

# Panel metrik interaktif
st.subheader("📈 Metrik Utama")
col1, col2, col3 = st.columns(3)
with col1:
    total_season = df_day_filtered["cnt"].sum()
    st.metric(f"Total {season_mapping[selected_season]}", f"{total_season:,}")

with col2:
    avg_hourly = hourly_counts["cnt"].mean()
    st.metric("Rata-rata per Jam", f"{avg_hourly:.0f}")

with col3:
    peak_hour = hourly_counts.loc[hourly_counts["cnt"].idxmax(), "hr"]
    st.metric("Jam Puncak", f"{int(peak_hour)}:00")

# Analisis tambahan
st.subheader("🔍 Insight Analisis")
st.write(f"""
1. **Pola Musiman**: {season_mapping[selected_season]} menunjukkan total penyewaan sebesar **{total_season:,}** sepeda
2. **Jam Sibuk**: Penyewaan tertinggi terjadi pada pukul **{int(peak_hour)}:00** dengan rata-rata **{avg_hourly:.0f}** sepeda
3. **Tren Harian**: Fluktuasi harian menunjukkan pola {'yang stabil' if df_day_filtered['cnt'].std() < 500 else 'variasi signifikan'}
""")