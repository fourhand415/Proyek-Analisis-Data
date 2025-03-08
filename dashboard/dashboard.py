import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Fungsi Input Data
def input_data():
    try:
        #Input Data Day
        data_day = pd.read_csv("data/day.csv")
        data_day["dteday"] = pd.to_datetime(data_day["dteday"])

        #Input Data Hour
        data_hour = pd.read_csv("data/hour.csv")
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


# Informasi Dasar
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Casual Overall", f"{data_day['casual'].sum():,}")
with col2:
    st.metric("Register Overall", f"{data_day['registered'].sum():,}")
with col3:
    st.metric("Total Penyewaan Sepeda", f"{data_day['cnt'].sum():,}")

# Pilih Musim
pilih_musim = st.sidebar.selectbox("Pilih Musim Untuk Data", data_day["season"].unique())
filter_data = data_day[data_day["season"] == pilih_musim]
filter_jam = data_hour[data_hour["season"] == pilih_musim]

# Informasi Dasar Musim
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Casual Musim", f"{filter_data['casual'].sum():,}")
with col2:
    st.metric("Register Musim", f"{filter_data['registered'].sum():,}")
with col3:
    st.metric("Total Penyewaan Sepeda Musim", f"{filter_data['cnt'].sum():,}")

# Visualisasi
st.subheader(f"Anda Memilih Musim {pilih_musim}, Pilih Visualisasi Dibawah")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Rata - Rata Penyewaan", "Total Penyewaan", "Rata - Rata per Jam", "Total per Jam", "Workingday", "Registered vs Casual"])

with tab1:
    st.subheader(f"Rata - Rata Penyewaan Sepeda di Musim {pilih_musim}")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=filter_data, x="weathersit", y="cnt", estimator="mean", ci=None, ax=ax, palette="viridis")
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Rata - Rata Penyewaan Sepeda")
    ax.set_title(f"Rata - Rata Penyewaan Sepeda di Musim {pilih_musim}")
    st.pyplot(fig)

with tab2:
    st.subheader(f"Total Penyewaan Sepeda di Musim {pilih_musim}")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=filter_data, x="weathersit", y="cnt", estimator=sum, ci=None, ax=ax, palette="viridis")
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Total Penyewaan Sepeda")
    ax.set_title(f"Total Penyewaan Sepeda di Musim {pilih_musim}")
    st.pyplot(fig)

with tab3:
    st.subheader(f"Rata - Rata Penyewaan Sepeda per Jam di Musim {pilih_musim}")
    agg_hour_avg = filter_jam.groupby('hr')['cnt'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.lineplot(data=agg_hour_avg, x = "hr", y = "cnt", marker="o", color = "green")
    plt.title("Average Penyewaan Sepeda per Jam")
    plt.xlabel("Jam")
    plt.ylabel("Avg Penyewaan")
    plt.xticks(range(0,24))
    st.pyplot(fig)

with tab4:
    st.subheader(f"Total Penyewaan Sepeda per Jam di Musim {pilih_musim}")
    agg_hour_sum = filter_jam.groupby('hr')['cnt'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data = agg_hour_sum, x = "hr", y = "cnt", color = "blue")
    plt.title("Total Penyewaan Sepeda per Jam")
    plt.xlabel("Jam")
    plt.ylabel("Sum Penyewaan")
    st.pyplot(fig)

with tab5:
    st.subheader(f"Total Penyewaan Sepeda di Musim {pilih_musim} Berdasarkan Working Day")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=filter_data, x="workingday", y="cnt", estimator=sum, ci=None, ax=ax, color="green")
    ax.set_xlabel("Working Day")
    ax.set_ylabel("Total Penyewaan Sepeda")
    ax.set_title(f"Total Penyewaan Sepeda di Musim {pilih_musim}")
    st.pyplot(fig)

with tab6:
    st.subheader(f"Total Penyewaan Sepeda di Musim {pilih_musim} (Registered vs Casual)")
    fig, ax = plt.subplots(figsize=(8, 5))
    agg_reg = filter_data.groupby("mnth")[["casual","registered"]].sum().reset_index()
    agg_reg_melted = agg_reg.melt(id_vars="mnth", var_name="Tipe Penyewa", value_name="Jumlah Penyewaan")
    month_labels = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
    agg_reg_melted["month_labels"] = agg_reg["mnth"].apply(lambda x: month_labels[x - 1])
    sns.barplot(x="month_labels", y="Jumlah Penyewaan", hue="Tipe Penyewa", data=agg_reg_melted, palette={"casual": "blue", "registered": "red"})
    ax.set_title(f"Total Penyewaan Sepeda Registered vs Casual di Musim {pilih_musim}")
    plt.xlabel("Bulan")
    plt.ylabel("Jumlah Penyewaan")
    plt.legend(title="Tipe Penyewa")
    st.pyplot(fig)