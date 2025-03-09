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

# Mapping angka musim ke nama musim
musim_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
df_day["season"] = df_day["season"].map(musim_map)

# Mapping kondisi cuaca
weather_map = {1: "Cerah", 2: "Berkabut/Berawan", 3: "Hujan Ringan", 4: "Hujan Deras"}
df_day["weathersit"] = df_day["weathersit"].map(weather_map)

# Sidebar untuk interaktif
st.sidebar.header("Filter Data")

# FITUR INTERAKTIF: Filter data berdasarkan rentang suhu
st.sidebar.subheader("Filter Rentang Suhu")
temp_min = float(df_day["temp"].min())
temp_max = float(df_day["temp"].max())
selected_temp_range = st.sidebar.slider(
    "Pilih Rentang Suhu (Normalisasi)",
    min_value=temp_min,
    max_value=temp_max,
    value=(temp_min, temp_max),
    step=0.05
)

# Filter seluruh dataset berdasarkan rentang suhu
df_day_temp_filtered = df_day[
    (df_day["temp"] >= selected_temp_range[0]) & 
    (df_day["temp"] <= selected_temp_range[1])
]

# Tambahkan filter musim sebagai pilihan kedua
selected_season = st.sidebar.selectbox(
    "Pilih Musim untuk Detail",
    options=list(musim_map.values())
)

# Filter berdasarkan musim dan suhu untuk visualisasi kedua
df_day_season_filtered = df_day_temp_filtered[df_day_temp_filtered["season"] == selected_season]

# Menampilkan header
st.header("📊 Dashboard Penyewaan Sepeda 🚲")
st.markdown(f"**Filter Aktif:** Rentang Suhu {selected_temp_range[0]:.2f}-{selected_temp_range[1]:.2f} (Normalisasi)")

# Visualisasi 1: Distribusi Penyewaan Antar Musim (Data Terfilter berdasarkan Suhu)
st.subheader(f"Distribusi Penyewaan Sepeda per Musim (Suhu: {selected_temp_range[0]:.2f}-{selected_temp_range[1]:.2f})")

# Hitung rata-rata penyewaan per musim untuk data terfilter
season_avg = df_day_temp_filtered.groupby("season")["cnt"].mean().reset_index()

fig1, ax1 = plt.subplots(figsize=(8,5))
sns.barplot(
    x='season',
    y='cnt',
    data=season_avg,
    palette="viridis",
    errorbar=None,
    ax=ax1
)
ax1.set_title(f"Distribusi Penyewaan Sepeda per Musim (Rentang Suhu: {selected_temp_range[0]:.2f}-{selected_temp_range[1]:.2f})")
ax1.set_xlabel("Musim")
ax1.set_ylabel("Rata-rata Penyewaan Harian")
plt.xticks(rotation=45)

# Tambahkan jumlah hari untuk setiap musim
for i, musim in enumerate(season_avg["season"]):
    count = len(df_day_temp_filtered[df_day_temp_filtered["season"] == musim])
    ax1.text(i, 10, f"{count} hari", ha='center', bbox=dict(facecolor='white', alpha=0.7))

st.pyplot(fig1)

# Visualisasi 2: Hubungan Suhu vs Penyewaan Sepeda (Data Terfilter)
st.subheader(f"Hubungan Suhu vs Penyewaan Sepeda ({selected_season})")
fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.scatterplot(
    data=df_day_season_filtered,
    x="temp", 
    y="cnt",
    hue="weathersit",
    palette="viridis",
    alpha=0.7,
    ax=ax2
)
ax2.set_title(f"Hubungan Suhu dengan Jumlah Penyewaan di {selected_season}")
ax2.set_xlabel("Suhu (Normalisasi)")
ax2.set_ylabel("Jumlah Penyewaan")
plt.legend(title="Kondisi Cuaca")
st.pyplot(fig2)

# Tampilkan metrik yang berubah berdasarkan filter
jumlah_data_musim = len(df_day_season_filtered)
if jumlah_data_musim > 0:
    # Panel metrik interaktif
    st.subheader("📈 Metrik Utama (Data Terfilter)")
    
    # Baris pertama metrik
    col1, col2, col3 = st.columns(3)
    with col1:
        # Jumlah hari terfilter
        jumlah_data_total = len(df_day_temp_filtered)
        st.metric("Total Hari (Semua Musim)", f"{jumlah_data_total}")
        
    with col2:
        # Rata-rata harian seluruh dataset terfilter
        avg_daily_all = df_day_temp_filtered["cnt"].mean()
        st.metric("Rata-rata Harian (Semua Musim)", f"{avg_daily_all:.0f}")
        
    with col3:
        # Suhu rata-rata
        avg_temp = df_day_temp_filtered["temp"].mean()
        # Konversi suhu dari normalisasi (0-1) ke Celcius untuk lebih mudah diinterpretasi
        # Asumsikan suhu dalam dataset sudah dinormalisasi dari -8°C hingga 39°C
        avg_temp_celcius = (avg_temp * 47) - 8
        st.metric("Suhu Rata-rata", f"{avg_temp_celcius:.1f}°C")
    
    # Baris kedua metrik (khusus musim terpilih)
    st.subheader(f"Detail untuk Musim {selected_season}")
    col1, col2, col3 = st.columns(3)
    with col1:
        total_rentals = df_day_season_filtered["cnt"].sum()
        st.metric(f"Total Penyewaan ({selected_season})", f"{total_rentals:,}")

    with col2:
        avg_daily = df_day_season_filtered["cnt"].mean()
        st.metric(f"Rata-rata Harian ({selected_season})", f"{avg_daily:.0f}")

    with col3:
        # Persentase dari total penyewaan
        percent_of_total = (total_rentals / df_day_temp_filtered["cnt"].sum() * 100).round(1)
        st.metric("% dari Total Penyewaan", f"{percent_of_total}%")

    # Tampilkan ringkasan data terfilter
    st.subheader("Ringkasan Data")
    
    # Buat tombol untuk mengubah tampilan
    show_option = st.radio("Tampilkan data berdasarkan:", ["Ringkasan per Kondisi Cuaca", "Data Detail"])
    
    if show_option == "Ringkasan per Kondisi Cuaca":
        ringkasan = df_day_season_filtered.groupby("weathersit")["cnt"].agg(["mean", "min", "max", "count"]).reset_index()
        ringkasan.columns = ["Kondisi Cuaca", "Rata-rata Penyewaan", "Minimum", "Maksimum", "Jumlah Hari"]
        st.write(ringkasan)
    else:
        st.write(df_day_season_filtered[["dteday", "temp", "weathersit", "cnt"]].sort_values(by="dteday"))
    
    # Analisis tambahan
    st.subheader("🔍 Insight Analisis")
    
    # Hitung hari dengan penyewaan tertinggi dan terendah
    if len(df_day_season_filtered) > 0:
        max_day = df_day_season_filtered.loc[df_day_season_filtered["cnt"].idxmax()]
        min_day = df_day_season_filtered.loc[df_day_season_filtered["cnt"].idxmin()]
        
        # Perbandingan antar musim
        season_comparison = df_day_temp_filtered.groupby("season")["cnt"].mean().reset_index()
        best_season = season_comparison.loc[season_comparison["cnt"].idxmax(), "season"]
        worst_season = season_comparison.loc[season_comparison["cnt"].idxmin(), "season"]
        
        st.write(f"""
        1. **Perbandingan Musim**: Dengan rentang suhu yang dipilih, **{best_season}** memiliki rata-rata penyewaan tertinggi dan **{worst_season}** terendah.
        2. **{selected_season}**: Terdapat **{jumlah_data_musim}** hari dalam rentang suhu yang dipilih dengan rata-rata penyewaan **{avg_daily:.0f}** sepeda per hari.
        3. **Hari Terbaik**: Penyewaan tertinggi terjadi pada **{max_day['dteday'].strftime('%d %B %Y')}** dengan **{max_day['cnt']}** sepeda (Cuaca: {max_day['weathersit']})
        4. **Hari Terburuk**: Penyewaan terendah terjadi pada **{min_day['dteday'].strftime('%d %B %Y')}** dengan **{min_day['cnt']}** sepeda (Cuaca: {min_day['weathersit']})
        """)
    else:
        st.warning(f"Tidak ada data untuk musim {selected_season} dalam rentang suhu yang dipilih.")
else:
    st.warning(f"Tidak ada data untuk musim {selected_season} dalam rentang suhu yang dipilih. Silakan sesuaikan rentang suhu.")