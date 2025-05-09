# Import Library
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from streamlit_lottie import st_lottie
import requests
import plotly.express as px

# Fungsi untuk mengambil animasi Lottie dari URL
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Ambil animasi Lottie
lottie_chart = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_tutvdkg0.json")

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Penjualan", layout="wide")

# Animasi dan Judul
with st.container():
    st_lottie(lottie_chart, height=180, key="top_analytics")

st.markdown("""
    <style>
    .main-title {
        font-size:48px !important;
        color:#00C49A;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .subtext {
        font-size:18px !important;
        color: #CFCFCF;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📊 Dashboard Analisis Penjualan</div>', unsafe_allow_html=True)
st.markdown('<div class="subtext">Laporan Interaktif Penjualan • Dibuat dengan Streamlit</div>', unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("Sample_Data_Analisis.csv")
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['month'] = df['order_date'].dt.to_period('M')
    df['total'] = df['price'] * df['quantity']
    return df

df = load_data()

# Sidebar Filter
st.sidebar.header("🔍 Filter Data")
selected_month = st.sidebar.selectbox("🗓️ Pilih Bulan:", sorted(df['month'].astype(str).unique()), index=0)
filtered_by_month = df[df['month'].astype(str) == selected_month]

selected_category = st.sidebar.multiselect(
    "📂 Pilih Kategori Produk:",
    options=filtered_by_month['category'].unique(),
    default=filtered_by_month['category'].unique()
)

filtered_df = filtered_by_month[filtered_by_month['category'].isin(selected_category)]

# Filter lokasi pelanggan jika tersedia
if 'customer_location' in df.columns:
    selected_location = st.sidebar.multiselect(
        "🏙️ Pilih Lokasi Pelanggan:",
        options=filtered_df['customer_location'].unique(),
        default=filtered_df['customer_location'].unique()
    )
    filtered_df = filtered_df[filtered_df['customer_location'].isin(selected_location)]

# Tab Konten
tab1, tab2 = st.tabs(["📈 Ringkasan", "📋 Data Lengkap"])

# Ringkasan
with tab1:
    st.subheader(f"📋 Ringkasan Data Bulan {selected_month}")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🧾 Total Transaksi", f"{len(filtered_df):,}")
    with col2:
        st.metric("📦 Produk Terjual", f"{int(filtered_df['quantity'].sum()):,}")
    with col3:
        st.metric("💰 Total Penjualan (Rp)", f"{filtered_df['total'].sum():,.0f}")

    st.subheader("📅 Total Penjualan per Bulan")
    monthly_sales = df.groupby('month')['total'].sum().reset_index()
    fig1 = px.line(monthly_sales, x='month', y='total', markers=True, title="Total Penjualan per Bulan", color_discrete_sequence=['#00C49A'])
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("🏆 10 Produk Terlaris")
    top_products = filtered_df.groupby('product_id')['quantity'].sum().sort_values(ascending=False).head(10).reset_index()
    fig2 = px.bar(top_products, x='product_id', y='quantity', title="10 Produk Terlaris", color='quantity', color_continuous_scale='Blues')
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📂 Penjualan per Kategori")
    top_categories = filtered_df.groupby('category')['quantity'].sum().reset_index().sort_values(by='quantity')
    fig3 = px.bar(top_categories, x='quantity', y='category', orientation='h', title="Penjualan per Kategori", color='quantity', color_continuous_scale='Teal')
    st.plotly_chart(fig3, use_container_width=True)

    if 'customer_location' in filtered_df.columns:
        st.subheader("📍 Penjualan per Lokasi Pelanggan")
        location_sales = filtered_df.groupby('customer_location')['total'].sum().reset_index().sort_values(by='total', ascending=False)
        fig4 = px.bar(location_sales, x='customer_location', y='total', title='Penjualan per Lokasi Pelanggan', color='total', color_continuous_scale='Agsunset')
        st.plotly_chart(fig4, use_container_width=True)

    st.subheader("💼 5 Penjual dengan Pendapatan Tertinggi")
    top_sellers = filtered_df.groupby('seller_id')['total'].sum().sort_values(ascending=False).head(5).reset_index()
    st.dataframe(top_sellers.rename(columns={'total': 'Total Penjualan'}))

# Tab Data Lengkap
with tab2:
    st.subheader("📋 Tabel Data Transaksi")
    st.dataframe(filtered_df)

    def convert_df_to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Data')
        return output.getvalue()

    excel_data = convert_df_to_excel(filtered_df)

    st.download_button(
        label="⬇️ Unduh Data ke Excel",
        data=excel_data,
        file_name="data_penjualan_filtered.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Footer
st.markdown("""
<hr style="border: 1px solid #555;">
<p style="text-align:center; color:gray;">
    🚀 Dibuat oleh Muhammad Syifa'ul Khuluq • Streamlit Dashboard © 2025
</p>
""", unsafe_allow_html=True)
