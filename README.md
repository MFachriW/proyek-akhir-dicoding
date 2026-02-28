# Proyek Analisis Data: E-Commerce Public Dataset 

## Deskripsi Proyek
Proyek ini merupakan *submission* akhir untuk kelas **Belajar Analisis Data dengan Python** di Dicoding. Proyek ini berfokus pada analisis data E-Commerce publik untuk menggali *insight* bisnis yang mencakup demografi pelanggan, metode pembayaran, analisis tingkat kepuasan, dan segmentasi pelanggan menggunakan metode RFM (*Recency, Frequency, Monetary*).

Selain analisis di Jupyter Notebook, proyek ini juga menyediakan *dashboard* interaktif yang dibangun menggunakan **Streamlit** untuk memvisualisasikan temuan data secara lebih dinamis.

## Struktur Direktori
- `/data`: Direktori yang berisi dataset mentah (format `.csv`) dari Olist.
- `/dashboard`: Direktori yang memuat kode *dashboard* (`dashboard.py`) dan dataset yang sudah dibersihkan (`main_data.csv`, `rfm_data.csv`, `review_data.csv`).
- `notebook.ipynb`: Berkas Jupyter Notebook yang berisi proses analisis data lengkap, mulai dari *Data Gathering*, *Assessing*, *Cleaning*, *Exploratory Data Analysis (EDA)*, hingga *Visualisasi dan Explanatory Analysis*.
- `README.md`: Dokumentasi petunjuk penggunaan proyek.
- `requirements.txt`: Daftar pustaka (*library*) Python yang dibutuhkan untuk menjalankan proyek.

## Cara Menjalankan Proyek (Setup Environment)

### 1. Instalasi Library
Pastikan Anda sudah menginstal Python di komputer Anda. Buka Terminal/Command Prompt, arahkan ke folder proyek ini, lalu jalankan perintah berikut untuk menyiapkan environment dan menginstal semua *library* yang dibutuhkan:

```bash
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

### 2. Menjalankan Dashboard Streamlit
Setelah instalasi selesai, jalankan perintah berikut di Terminal/Command Prompt untuk membuka *dashboard*:

```bash
streamlit run dashboard/dashboard.py
```

Sistem secara otomatis akan membuka dashboard interaktif di browser bawaan Anda.