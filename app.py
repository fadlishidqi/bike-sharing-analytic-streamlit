import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Dataset characteristics
day_df = pd.read_csv('data/day.csv')
hour_df = pd.read_csv('data/hour.csv')

## Streamlit app title
st.title("Bike Sharing Data Analysis")
st.subheader("By Fadli Shidqi Firdaus")

st.markdown("""
## Pengantar
Analisis ini bertujuan untuk memahami pola penggunaan layanan bike sharing dan faktor-faktor yang mempengaruhinya.
Kita akan menjelajahi data harian dan per jam untuk mendapatkan wawasan yang berharga.
""")

# Menampilkan 5 data teratas dari data day
st.subheader("Data Preview - Day")
st.write(day_df.head())

# Menampilkan 5 data teratas dari data hour
st.subheader("Data Preview - Hour")
st.write(hour_df.head())

st.markdown("""
## Data Cleaning
Pada tahap ini, kita membersihkan data dengan menghapus kolom yang tidak diperlukan, 
mengubah nama kolom untuk memperjelas data, dan mengkonversi tipe data yang sesuai.
""")

# Cleaning Data
day_df = day_df.drop(columns=['workingday', 'instant', 'atemp', 'holiday'])
hour_df = hour_df.drop(columns=['workingday', 'instant', 'atemp', 'holiday'])

# Mengubah nama kolom untuk memperjelas data
day_df.rename(columns={
    'yr': 'year',
    'dteday': 'date_day',
    'mnth': 'month',
    'weekday': 'day',
    'weathersit': 'weather_situation',
    'windspeed': 'wind_speed',
    'cnt': 'count_total',
    'hum': 'humidity',
    'temp': 'temperature',
    'casual': 'casual_users',
    'registered': 'registered_users',
}, inplace=True)

hour_df.rename(columns={
    'yr': 'year',
    'dteday': 'date_day',
    'mnth': 'month',
    'weathersit': 'weather_situation',
    'windspeed': 'wind_speed',
    'cnt': 'count_total',
    'hum': 'humidity',
    'temp': 'temperature',
    'casual': 'casual_users',
    'registered': 'registered_users',
    'hr': 'hour',
    'weekday': 'day',
}, inplace=True)

# Mengubah tipe data kolom 'date_day' menjadi datetime
day_df['date_day'] = pd.to_datetime(day_df['date_day'])
hour_df['date_day'] = pd.to_datetime(hour_df['date_day'])

columns = ['season', 'month', 'day', 'weather_situation']
for column in columns:
    day_df[column] = day_df[column].astype("category")
    hour_df[column] = hour_df[column].astype("category")

# Konversi nilai
season_mapping = {1: 'Semi', 2: 'Panas', 3: 'Gugur', 4: 'Salju'}
day_df['season'] = day_df['season'].map(season_mapping)
hour_df['season'] = hour_df['season'].map(season_mapping)

weather_mapping = {1: 'Cerah', 2: 'Berkabut', 3: 'Hujan_Salju_Ringan', 4: 'Hujan_Salju_Lebat'}
day_df['weather_situation'] = day_df['weather_situation'].map(weather_mapping)
hour_df['weather_situation'] = hour_df['weather_situation'].map(weather_mapping)

month_mapping = {1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April', 5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Agustus', 9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'}
day_df['month'] = day_df['month'].map(month_mapping)
hour_df['month'] = hour_df['month'].map(month_mapping)

day_mapping = {0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'}
day_df['day'] = day_df['day'].map(day_mapping)
hour_df['day'] = hour_df['day'].map(day_mapping)

year_mapping = {0: '2011', 1: '2012'}
day_df['year'] = day_df['year'].map(year_mapping)
hour_df['year'] = hour_df['year'].map(year_mapping)

hour_df['hour'] = hour_df['hour'].apply(lambda x: '{:02d}:00'.format(x))

# Konversi temperature, humidity, windspeed ke nilai aslinya
hour_df['temperature'] = (hour_df['temperature'] * 41).round().astype(int)
hour_df['humidity'] = (hour_df['humidity'] * 100).round().astype(int)
hour_df['wind_speed'] = (hour_df['wind_speed'] * 67).round().astype(int)

day_df['temperature'] = (day_df['temperature'] * 41).round().astype(int)
day_df['humidity'] = (day_df['humidity'] * 100).round().astype(int)
day_df['wind_speed'] = (day_df['wind_speed'] * 67).round().astype(int)

# Menampilkan data yang telah dibersihkan di Streamlit
st.write("Data day.csv yang sudah dibersihkan:")
st.write(day_df.head())

st.write("Data hour.csv yang sudah dibersihkan:")
st.write(hour_df.head())

st.markdown("""
## Exploratory Data Analysis
Berikut adalah analisis eksploratori untuk memahami pola penggunaan sepeda berdasarkan 
berbagai faktor seperti hari, jam, musim, dan kondisi cuaca.
""")

# EDA: Di hari apa pengguna paling sering meminjam sepeda?
st.subheader("Di hari apa pengguna paling sering meminjam sepeda?")
weekday_rentals = day_df.groupby('day')['count_total'].sum().reset_index()
most_rentals_day = weekday_rentals.loc[weekday_rentals['count_total'].idxmax()]
least_rentals_day = weekday_rentals.loc[weekday_rentals['count_total'].idxmin()]
st.write(f"Hari dengan penyewaan sepeda tertinggi: {most_rentals_day['day']}, dengan total {most_rentals_day['count_total']}")
st.write(f"Hari dengan penyewaan sepeda terendah: {least_rentals_day['day']}, dengan total {least_rentals_day['count_total']}")

# EDA: Pada jam berapa menunjukkan lonjakan terbesar?
st.subheader("Pada jam berapa lonjakan penyewaan terbesar?")
hourly_rentals = hour_df.groupby('hour')['count_total'].sum().reset_index()
peak_hour = hourly_rentals.loc[hourly_rentals['count_total'].idxmax()]
st.write(f"Jam dengan penyewaan sepeda tertinggi: {peak_hour['hour']}, dengan total {peak_hour['count_total']}")

# EDA: Musim apa yang paling populer?
st.subheader("Musim mana yang paling populer untuk penyewaan sepeda?")
season_rentals = day_df.groupby('season')['count_total'].sum().reset_index()
popular_season = season_rentals.loc[season_rentals['count_total'].idxmax()]
st.write(f"Musim paling populer untuk penyewaan sepeda: {popular_season['season']}, dengan total {popular_season['count_total']}")

# Tetapkan palet warna
color_palette = sns.color_palette("husl", 8)
sns.set_palette(color_palette)

# Visualisasi penyewaan sepeda berdasarkan hari
st.subheader("Visualisasi penyewaan sepeda berdasarkan hari")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='day', y='count_total', data=weekday_rentals, ax=ax)
ax.set_title("Jumlah Penyewaan Sepeda per Hari", fontsize=16)
ax.set_xlabel("Hari", fontsize=12)
ax.set_ylabel("Jumlah Penyewaan", fontsize=12)
st.pyplot(fig)

# Visualisasi penyewaan sepeda berdasarkan jam
st.subheader("Visualisasi penyewaan sepeda berdasarkan jam")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='hour', y='count_total', data=hourly_rentals, ax=ax, marker="o", linewidth=2)
ax.set_title("Jumlah Penyewaan Sepeda per Jam", fontsize=16)
ax.set_xlabel("Jam", fontsize=12)
ax.set_ylabel("Jumlah Penyewaan", fontsize=12)
st.pyplot(fig)

# Visualisasi penyewaan sepeda berdasarkan musim
st.subheader("Visualisasi penyewaan sepeda berdasarkan musim")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='season', y='count_total', data=season_rentals, ax=ax)
ax.set_title("Jumlah Penyewaan Sepeda per Musim", fontsize=16)
ax.set_xlabel("Musim", fontsize=12)
ax.set_ylabel("Jumlah Penyewaan", fontsize=12)
st.pyplot(fig)

# Korelasi antara suhu dan penyewaan sepeda
st.subheader("Apakah ada hubungan antara penyewa sepeda dengan suhu dan cuaca?")
correlation_temp = day_df[['temperature', 'count_total']].corr().iloc[0, 1]
st.write(f"Korelasi antara suhu dan penyewaan sepeda: {correlation_temp:.2f}")
weather_rentals = day_df.groupby('weather_situation')['count_total'].mean().reset_index()
st.write(weather_rentals)

# Visualisasi rata-rata penyewaan sepeda berdasarkan kondisi cuaca
st.subheader("Visualisasi rata-rata penyewaan sepeda berdasarkan kondisi cuaca")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='weather_situation', y='count_total', data=weather_rentals, ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda berdasarkan Kondisi Cuaca", fontsize=16)
ax.set_xlabel("Kondisi Cuaca", fontsize=12)
ax.set_ylabel("Rata-rata Jumlah Penyewaan", fontsize=12)
st.pyplot(fig)

# Pengguna berlangganan atau tidak?
st.subheader("Lebih banyak mana: pengguna berlangganan atau tidak?")
subscription_rentals = day_df[['registered_users', 'casual_users']].sum().reset_index()
subscription_rentals.columns = ['user_type', 'total_rentals']
st.write(subscription_rentals)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='user_type', y='total_rentals', data=subscription_rentals, ax=ax)
ax.set_title("Perbandingan Jumlah Penyewaan: Pengguna Berlangganan vs Kasual", fontsize=16)
ax.set_xlabel("Tipe Pengguna", fontsize=12)
ax.set_ylabel("Total Penyewaan", fontsize=12)
st.pyplot(fig)

# Analisis Lanjutan - Clustering Manual
st.subheader("Analisis Lanjutan - Clustering Manual")

st.markdown("""
Kita akan melakukan clustering manual berdasarkan durasi perjalanan untuk memahami 
pola penggunaan sepeda berdasarkan lama waktu penyewaan.
""")

def categorize_duration(duration):
    if duration <= 10:
        return 'Perjalanan Singkat'
    elif 10 < duration <= 30:
        return 'Perjalanan Menengah'
    else:
        return 'Perjalanan Panjang'

# Asumsikan 'duration' adalah dalam menit dan dihitung dari 'count_total'
hour_df['duration'] = hour_df['count_total'] / 60  # Asumsi 1 count = 1 menit
hour_df['duration_category'] = hour_df['duration'].apply(categorize_duration)

# Analisis hasil clustering
cluster_stats = hour_df.groupby('duration_category').agg({
    'count_total': 'count',
    'duration': ['mean', 'median'],
    'temperature': 'mean'
})

cluster_stats.columns = ['count', 'duration_mean', 'duration_median', 'temperature_mean']
cluster_stats = cluster_stats.reset_index()

st.write("Statistik Cluster Durasi Perjalanan:")
st.write(cluster_stats)

# Visualisasi hasil clustering
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='duration_category', y='count', data=cluster_stats, ax=ax)
ax.set_title("Distribusi Kategori Durasi Perjalanan", fontsize=16)
ax.set_xlabel("Kategori Durasi", fontsize=12)
ax.set_ylabel("Jumlah Perjalanan", fontsize=12)
st.pyplot(fig)

# Temukan kategori dengan jumlah perjalanan terbanyak
most_common_category = cluster_stats.loc[cluster_stats['count'].idxmax(), 'duration_category']

# Temukan kategori dengan rata-rata durasi terpanjang
longest_duration_category = cluster_stats.loc[cluster_stats['duration_mean'].idxmax(), 'duration_category']

# Temukan kategori dengan rata-rata suhu tertinggi
highest_temp_category = cluster_stats.loc[cluster_stats['temperature_mean'].idxmax(), 'duration_category']

st.markdown(f"""
### Interpretasi Hasil Clustering
- Kategori perjalanan yang paling umum adalah {most_common_category}.
- Rata-rata durasi perjalanan terpanjang terjadi pada kategori {longest_duration_category}.
- Kategori {highest_temp_category} memiliki rata-rata suhu tertinggi.

Informasi ini dapat digunakan untuk:
1. Menyesuaikan tarif berdasarkan durasi perjalanan.
2. Mengoptimalkan distribusi sepeda berdasarkan pola durasi perjalanan.
3. Merancang promosi khusus untuk mendorong penggunaan pada kategori durasi tertentu.
4. Mempertimbangkan faktor cuaca dalam strategi penyediaan sepeda untuk berbagai durasi perjalanan.
""")

# Kesimpulan
# Tambahkan kode ini di bagian akhir file Streamlit Anda

st.subheader("Kesimpulan Analisis Data")

st.markdown(f"""
Berdasarkan analisis yang telah dilakukan, berikut kesimpulan utama yang menjawab pertanyaan bisnis:

1. **Pola Penggunaan Sepeda:**
   - Hari dengan penyewaan tertinggi adalah {most_rentals_day['day']}, sementara terendah adalah {least_rentals_day['day']}.
   - Jam puncak penyewaan adalah pada pukul {peak_hour['hour']}.
   - Musim {popular_season['season']} adalah yang paling populer untuk penyewaan sepeda.

2. **Faktor yang Mempengaruhi Permintaan:**
   - Terdapat korelasi positif antara suhu dan jumlah penyewaan sepeda (korelasi: {correlation_temp:.2f}).
   - Kondisi cuaca mempengaruhi rata-rata penyewaan sepeda, dengan cuaca {weather_rentals.loc[weather_rentals['count_total'].idxmax(), 'weather_situation']} menunjukkan penyewaan tertinggi.

3. **Profil Pengguna:**
   - Pengguna berlangganan (registered users) lebih banyak dibandingkan pengguna kasual.

4. **Pola Durasi Perjalanan:**
   - Kategori perjalanan yang paling umum adalah {most_common_category}.
   - Rata-rata durasi perjalanan terpanjang terjadi pada kategori {longest_duration_category}.

5. **Rekomendasi Bisnis:**
   - Tingkatkan ketersediaan sepeda pada hari {most_rentals_day['day']} dan sekitar pukul {peak_hour['hour']}.
   - Fokuskan promosi pada musim {popular_season['season']} untuk memaksimalkan penyewaan.
   - Pertimbangkan strategi untuk meningkatkan jumlah pengguna berlangganan.
   - Siapkan rencana kontingensi untuk kondisi cuaca yang kurang favorable.
   - Sesuaikan tarif dan strategi pemasaran berdasarkan kategori durasi perjalanan.

Kesimpulan ini dapat digunakan untuk mengoptimalkan operasional dan strategi pemasaran layanan bike sharing.
""")