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

# Menampilkan 5 data teratas dari data day
st.subheader("Data Preview - Day")
st.write(day_df.head())

# Menampilkan 5 data teratas dari data hour
st.subheader("Data Preview - Hour")
st.write(hour_df.head())

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

# Visualisasi penyewaan sepeda berdasarkan hari
st.subheader("Visualisasi penyewaan sepeda berdasarkan hari")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='day', y='count_total', data=weekday_rentals, ax=ax)
st.pyplot(fig)

# Visualisasi penyewaan sepeda berdasarkan jam
st.subheader("Visualisasi penyewaan sepeda berdasarkan jam")
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x='hour', y='count_total', data=hourly_rentals, ax=ax, marker="o", color='red')
st.pyplot(fig)

# Visualisasi penyewaan sepeda berdasarkan musim
st.subheader("Visualisasi penyewaan sepeda berdasarkan musim")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='season', y='count_total', data=season_rentals, ax=ax)
st.pyplot(fig)

# Korelasi antara suhu dan penyewaan sepeda
st.subheader("Apakah ada hubungan antara penyewa sepeda dengan suhu dan cuaca?")
correlation_temp = day_df[['temperature', 'count_total']].corr().iloc[0, 1]
st.write(f"Korelasi antara suhu dan penyewaan sepeda: {correlation_temp:.2f}")
weather_rentals = day_df.groupby('weather_situation')['count_total'].mean().reset_index()
st.write(weather_rentals)

# Visualisasi rata-rata penyewaan sepeda berdasarkan kondisi cuaca
st.subheader("Visualisasi rata-rata penyewaan sepeda berdasarkan kondisi cuaca")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='weather_situation', y='count_total', data=weather_rentals, ax=ax)
st.pyplot(fig)

# Pengguna berlangganan atau tidak?
st.subheader("Lebih banyak mana: pengguna berlangganan atau tidak?")
subscription_rentals = day_df[['registered_users', 'casual_users']].sum().reset_index()
subscription_rentals.columns = ['user_type', 'total_rentals']
st.write(subscription_rentals)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='user_type', y='total_rentals', data=subscription_rentals, ax=ax)
st.pyplot(fig)
