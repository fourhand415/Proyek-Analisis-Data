# Proyek Belajar Analisis Data dengan Python : Dataset Bike Sharing

## Deskripsi Proyek
Proyek ini bertujuan untuk menganalisis dataset untuk memperoleh sebuah insight. Hasil analisis divisualisasikan dalam dashboard interaktif menggunakan **Streamlit**.

## 📂 Struktur Direktori
```
Proyek-Analisis-Data/
│── dashboard/
│   ├── dashboard.py
│── data/
│   ├── day.csv
│   ├── hour.csv
│   ├── Readme.txt
│── Proyek_Analisis_Data.ipynb
│── README.md
│── requirements.txt
│── url.txt
```

## Cara Menjalankan Dashboard
1. **Pastikan Python sudah terinstal**
2. **Clone Repository**
   ```bash
   https://github.com/fourhand415/Proyek-Analisis-Data.git
   ```
3. **Install Library yang digunakan**
   ```bash
   pip install pandas matplotlib seaborn streamlit
   ```
   atau bisa menggunakan file requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```
4. **Select Directory**
   ```bash
   cd Proyek-Analisis-Data/dashboard
   ```
5. **Jalankan Dashboard**
   ```bash
   streamlit run dashboard.py
   ```
6. **Buka di browser**
   - Streamlit akan berjalan di `https://proyek-dashboard-bike-analysis.streamlit.app/`
