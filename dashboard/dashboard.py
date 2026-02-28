import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Fachri Online Store", page_icon="🛒", layout="wide")
sns.set(style='whitegrid') 

# --- LOAD DATA ---
@st.cache_data
def load_data():
    main_df = pd.read_csv("dashboard/main_data.csv")
    rfm_df = pd.read_csv("dashboard/rfm_data.csv")
    review_df = pd.read_csv("dashboard/review_data.csv")
    
    datetime_columns = ["order_purchase_timestamp"]
    for col in datetime_columns:
        if col in main_df.columns:
            main_df[col] = pd.to_datetime(main_df[col])
        if col in review_df.columns:
            review_df[col] = pd.to_datetime(review_df[col])
            
    # Membuat ID pendek untuk visualisasi RFM agar teks tidak tumpang tindih
    if "customer_id" in rfm_df.columns:
        rfm_df["short_id"] = rfm_df["customer_id"].astype(str).str[:8]
    elif "customer_unique_id" in rfm_df.columns:
        rfm_df["short_id"] = rfm_df["customer_unique_id"].astype(str).str[:8]
        
    return main_df, rfm_df, review_df

main_data, rfm_data, review_data = load_data()

# --- SIDEBAR (FILTER) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 120px;'>🛒</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; font-size: 20px;'>Fachri Online Store</h3>", unsafe_allow_html=True)
    
    st.write("---") 
    st.write("") 
    st.write("")
    st.write("### Silakan pilih tanggal yang ingin diikutkan dalam analisis")
    st.write("")
    st.write("")
    
    # Gunakan try-except untuk mencegah error saat pengguna mengatur tanggal
    try:
        start_date, end_date = st.date_input(
            label='Rentang Waktu Analysis',
            min_value=main_data["order_purchase_timestamp"].min().date(),
            max_value=main_data["order_purchase_timestamp"].max().date(),
            value=[main_data["order_purchase_timestamp"].min().date(), main_data["order_purchase_timestamp"].max().date()],
            help="Pilih rentang tanggal untuk memfilter data yang akan dianalisis. Pastikan memilih tanggal awal dan akhir."
        )
    except ValueError:
        st.error("Pastikan memilih rentang tanggal yang lengkap (Awal dan Akhir).")
        st.stop()

# Filter Dataframe berdasarkan tanggal
main_df_filtered = main_data[(main_data["order_purchase_timestamp"].dt.date >= start_date) & 
                             (main_data["order_purchase_timestamp"].dt.date <= end_date)]

review_df_filtered = review_data[(review_data["order_purchase_timestamp"].dt.date >= start_date) & 
                                 (review_data["order_purchase_timestamp"].dt.date <= end_date)]

# Fungsi bantuan untuk membuat palet warna (1 highlight, sisanya abu-abu)
def get_color_palette(n_colors):
    return ["#72BCD4"] + ["#D3D3D3"] * (n_colors - 1)

# --- DASHBOARD MAIN PAGE ---
st.header('Fachri E-Commerce Analytics Dashboard :sparkles:')
st.markdown("---")

# =========================================
# BAGIAN 1: DEMOGRAFI & PEMBAYARAN (Q1 & Q2)
# =========================================
st.subheader("Demografi Pelanggan & Metode Pembayaran")
col1, col2 = st.columns(2)

with col1:
    st.write("**Top 5 States by Customers**")
    state_counts = main_df_filtered.groupby("customer_state").customer_id.nunique().sort_values(ascending=False).head(5)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=state_counts.values, y=state_counts.index, palette=get_color_palette(len(state_counts)), ax=ax)
    ax.set_xlabel("Jumlah Pelanggan")
    ax.set_ylabel("Negara Bagian")
    st.pyplot(fig)
    
with col2:
    st.write("**Top 5 Payment Methods**")
    pay_counts = main_df_filtered.groupby("payment_type").order_id.nunique().sort_values(ascending=False).head(5)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=pay_counts.values, y=pay_counts.index, palette=get_color_palette(len(pay_counts)), ax=ax)
    ax.set_xlabel("Jumlah Transaksi")
    ax.set_ylabel("Metode Pembayaran")
    st.pyplot(fig)
    

st.markdown("---")

# =========================================
# BAGIAN 2: KEPUASAN PELANGGAN (Q3)
# =========================================
st.subheader("Kepuasan Pelanggan (Rating vs Durasi Pengiriman)")
avg_review = review_df_filtered.review_score.mean()
st.metric("Average Review Score", value=f"{avg_review:.2f} / 5.0")

urutan_waktu = ['Sangat Cepat (0-6 hari)', 'Normal (7-15 hari)', 'Lambat (16-30 hari)', 'Sangat Lambat (31-60 hari)', 'Ekstrem (>60 hari)'] 
rata_rata_kategori = review_df_filtered.groupby('duration_category')['review_score'].mean()
dua_terendah = rata_rata_kategori.nsmallest(2).index.tolist()

warna_kustom = []
for kategori in urutan_waktu:
    if kategori in dua_terendah:
        warna_kustom.append("#E74C3C") # Merah untuk highlight buruk
    else:
        warna_kustom.append("#D3D3D3") # Abu-abu untuk yang aman

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    x='duration_category', 
    y='review_score', 
    data=review_df_filtered, 
    order=urutan_waktu,       
    palette=warna_kustom,     
    ax=ax
)

# Memutar teks 45 derajat agar tidak tumpang tindih
plt.xticks(rotation=45, ha='right')

ax.set_xlabel("Durasi Pengiriman")
ax.set_ylabel("Rata-rata Skor Ulasan")
st.pyplot(fig)

st.markdown("---")
# =========================================
# BAGIAN 3: ANALISIS RFM (Q4 & Q5)
# =========================================
st.subheader("Performa Pelanggan (RFM Analysis)")

# Menampilkan Rata-rata Parameter RFM
col1, col2, col3 = st.columns(3)
col1.metric("Average Recency", f"{rfm_data.recency.mean():.1f} Days")
col2.metric("Average Frequency", f"{rfm_data.frequency.mean():.2f} Orders")
col3.metric("Average Monetary", f"Unit {rfm_data.monetary.mean():.2f}")

st.write("---")
st.write("**Best Customers Based on RFM Parameters**")

# Visualisasi Top 5 Pelanggan per Parameter RFM
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 10))
rfm_colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"] # 1 Highlight, 4 Abu-abu

# Grafik Recency (Nilai terkecil/terbaru adalah yang terbaik)
top_recency = rfm_data.sort_values(by="recency", ascending=True).head(5)
sns.barplot(x="recency", y="short_id", data=top_recency, palette=rfm_colors, ax=ax[0])
ax[0].set_title("By Recency (Hari)", loc="center", fontsize=18)
ax[0].set_ylabel("Customer ID")
ax[0].set_xlabel("")

# Grafik Frequency (Nilai terbesar adalah yang terbaik)
top_frequency = rfm_data.sort_values(by="frequency", ascending=False).head(5)
sns.barplot(x="frequency", y="short_id", data=top_frequency, palette=rfm_colors, ax=ax[1])
ax[1].set_title("By Frequency (Jumlah Order)", loc="center", fontsize=18)
ax[1].set_ylabel("")
ax[1].set_xlabel("")

# Grafik Monetary (Nilai terbesar adalah yang terbaik)
top_monetary = rfm_data.sort_values(by="monetary", ascending=False).head(5)
sns.barplot(x="monetary", y="short_id", data=top_monetary, palette=rfm_colors, ax=ax[2])
ax[2].set_title("By Monetary (Total Pengeluaran)", loc="center", fontsize=18)
ax[2].set_ylabel("")
ax[2].set_xlabel("")

st.pyplot(fig)

st.write("---")

# =========================================
# GRAFIK TAMBAHAN: JUMLAH PELANGGAN & REVENUE PER KATEGORI
# =========================================
if "customer_segment" in rfm_data.columns:
    st.write("**Komposisi Segmen Pelanggan & Kontribusi Revenue (Q4 & Q5)**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Grafik 1: Jumlah Pelanggan per Segmen
        segment_counts = rfm_data['customer_segment'].value_counts().reset_index()
        segment_counts.columns = ['customer_segment', 'customer_count']
        
        # Highlight kategori dengan pelanggan terbanyak (Low Value / Medium Value)
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        sns.barplot(x='customer_count', y='customer_segment', data=segment_counts, 
                    palette=["#72BCD4"] + ["#D3D3D3"] * (len(segment_counts)-1), ax=ax1)
        ax1.set_title("Jumlah Pelanggan per Segmen", fontsize=14)
        ax1.set_xlabel("Jumlah Pelanggan")
        ax1.set_ylabel("")
        st.pyplot(fig1)

    with col2:
        # Grafik 2: Revenue per Segmen
        segment_revenue = rfm_data.groupby('customer_segment')['monetary'].sum().reset_index()
        segment_revenue = segment_revenue.sort_values(by='monetary', ascending=False)
        
        # Highlight kategori dengan revenue terbesar
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        sns.barplot(x='monetary', y='customer_segment', data=segment_revenue, 
                    palette=["#72BCD4"] + ["#D3D3D3"] * (len(segment_revenue)-1), ax=ax2)
        ax2.set_title("Total Revenue per Segmen", fontsize=14)
        ax2.set_xlabel("Total Revenue (Unit)")
        ax2.set_ylabel("")
        st.pyplot(fig2)

st.caption('Copyright (c) Muhamad Fachri Wijaya 2026')