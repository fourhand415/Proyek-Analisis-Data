import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Fungsi Input Data
def input_data():
    try:
        #Input Data Day
        data_day = pd.read_csv("e:/ITS/Coding Camp/Belajar/8. Modul Belajar Analisis Data dengan Python/Proyek-Analisis-Data/data/day.csv")
        data_day["dteday"] = pd.to_datetime(data_day["dteday"])

        #Input Data Hour
        data_hour = pd.read_csv("e:/ITS/Coding Camp/Belajar/8. Modul Belajar Analisis Data dengan Python/Proyek-Analisis-Data/data/hour.csv")
        data_hour["dteday"] = pd.to_datetime(data_hour["dteday"])

        # Mapping kategori `season` dan `weathersit`
        for df in [data_day, data_hour]:
            df["season"] = df["season"].map({1:"Spring", 2:"Summer", 3:"Fall", 4:"Winter"})
            df["weathersit"] = df["weathersit"].map({1:"Clear", 2:"Mist + Cloudy", 3:"Light Snow", 4:"Heavy Rain"})
        return data_day,data_hour
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame()

data_day, data_hour = input_data()

# Title
st.title("Dashboard Bike Sharing")

# Pilih Musim Termasuk All Seasons
all_seasons_option = "All Seasons"
season_options = [all_seasons_option] + list(data_day["season"].unique())

pilih_musim = st.sidebar.multiselect("Pilih Musim Untuk Data", season_options, default=season_options[1:])

# Jika "All Seasons" dipilih, hanya itu yang boleh dipilih
if all_seasons_option in pilih_musim:
    pilih_musim = [all_seasons_option]
else:
    pilih_musim = [season for season in pilih_musim if season != all_seasons_option]

# Filter data berdasarkan musim yang dipilih
if all_seasons_option in pilih_musim:
    filter_data = data_day 
    filter_jam = data_hour
else:
    filter_data = data_day[data_day["season"].isin(pilih_musim)]
    filter_jam = data_hour[data_hour["season"].isin(pilih_musim)]

pilih_musim = ", ".join(pilih_musim)

# Informasi Dasar Musim
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Casual", f"{filter_data['casual'].sum():,}")
with col2:
    st.metric("Register", f"{filter_data['registered'].sum():,}")
with col3:
    st.metric("Total Penyewaan Sepeda", f"{filter_data['cnt'].sum():,}")

# Visualisasi
st.subheader(f"Anda Memilih Musim {pilih_musim}, Pilih Visualisasi Dibawah")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Rata - Rata Berdasarkan Musim", "Rata - Rata Berdasarkan Cuaca", "Rata - Rata per Jam", "Total per Jam", "Workingday", "Jam dan Hari"])

with tab1:
    st.subheader(f"Rata - Rata Penyewaan Sepeda Berdasarkan Musim")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=filter_data, x="season", y="cnt", ci=None, ax=ax, color="blue")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata - Rata Penyewaan Sepeda")
    ax.set_title(f"Rata - Rata Penyewaan Sepeda di Musim {pilih_musim}")
    st.pyplot(fig)

with tab2:
    st.subheader(f"Rata - Rata Penyewaan Sepeda Berdasarkan Cuaca")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=filter_data, x="weathersit", y="cnt", ci=None, ax=ax, color="green")
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Rata - Rata Penyewaan Sepeda")
    ax.set_title(f"Rata - Rata Penyewaan Sepeda Berdasarkan Cuaca")
    st.pyplot(fig)

with tab3:
    st.subheader(f"Rata - Rata Penyewaan Sepeda per Jam di Musim {pilih_musim}")
    agg_hour_avg = filter_jam.groupby('hr')['cnt'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.lineplot(data=agg_hour_avg, x = "hr", y = "cnt", marker="o", color = "blue")
    plt.title("Average Penyewaan Sepeda per Jam")
    plt.xlabel("Jam")
    plt.ylabel("Avg Penyewaan")
    plt.xticks(range(0,24))
    st.pyplot(fig)

with tab4:
    st.subheader(f"Total Penyewaan Sepeda per Jam di Musim {pilih_musim}")
    agg_hour_sum = filter_jam.groupby('hr')['cnt'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data = agg_hour_sum, x = "hr", y = "cnt", color = "green")
    plt.title("Total Penyewaan Sepeda per Jam")
    plt.xlabel("Jam")
    plt.ylabel("Sum Penyewaan")
    st.pyplot(fig)

with tab5:
    st.subheader(f"Tren Penyewaan Sepeda di Musim {pilih_musim} Berdasarkan Working Day")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.lineplot(x = 'dteday', y = "cnt", data = filter_data, hue = 'workingday', palette = "Set1")
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Penyewaan Sepeda")
    plt.xticks(rotation = 60)
    ax.set_title(f"Tren Penyewaan Sepeda Berdasarkan Workingday (Hari Kerja (1), Libur (0) )")
    st.pyplot(fig)

with tab6:
    st.subheader(f"Total Penyewaan Sepeda di Musim {pilih_musim} Berdasarkan Jam dan Hari")
    # Mapping hari dan Atur kategori jam
    day_mapping = {
        0: "Minggu", 1: "Senin", 2: "Selasa", 3: "Rabu", 4: "Kamis", 5: "Jumat", 6: "Sabtu"}
    
    def categorize_time(hour):
        if 6 <= hour < 11:
            return "Pagi"
        elif 11 <= hour < 16:
            return "Siang"
        elif 16 <= hour < 20:
            return "Sore"
        else:
            return "Malam"
    
    filter_jam["time_category"] = filter_jam["hr"].apply(categorize_time)
    filter_jam["day_name"] = filter_jam["weekday"].map(day_mapping)

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x="day_name", y="cnt", hue="time_category", data=filter_jam, 
                order=["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"],
                palette="Blues", ci = None)
    ax.set_title(f"Total Penyewaan Sepeda di Musim {pilih_musim} Berdasarkan Jam dan Hari")
    plt.xlabel("Hari")
    plt.ylabel("Jumlah Peminjaman Sepeda")
    plt.legend(title="Waktu Penggunaan")
    st.pyplot(fig)
