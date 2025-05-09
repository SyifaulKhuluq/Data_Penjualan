import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Dashboard Penjualan", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data_penjualan.csv")
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["month"] = df["order_date"].dt.to_period('M').astype(str)
    return df

df = load_data()

# Sidebar - Filter
st.sidebar.header("Filter")
all_months = sorted(df["month"].unique())
selected_month = st.sidebar.selectbox("📅 Pilih Bulan:", all_months, index=len(all_months)-1)
filtered_by_month = df[df["month"] == selected_month]

locations = sorted(filtered_by_month["customer_location"].dropna().unique())
selected_locations = st.sidebar.multiselect("🏙️ Pilih Lokasi Pelanggan:", options=locations, default=locations)
filtered_df = filtered_by_month[filtered_by_month["customer_location"].isin(selected_locations)]

# Header
st.title("📊 Dashboard Penjualan")
st.markdown(f"### Bulan: {selected_month}")

# KPI Metrics
monthly_totals = df.groupby('month')['total'].sum().sort_index()
current = monthly_totals[selected_month]
prev_index = monthly_totals.index.get_loc(selected_month) - 1
previous = monthly_totals.iloc[prev_index] if prev_index >= 0 else 0
growth = ((current - previous) / previous * 100) if previous != 0 else 0

col1, col2 = st.columns(2)
with col1:
    st.metric("💰 Total Penjualan", f"Rp {current:,.0f}", delta=f"Rp {current - previous:,.0f}")
with col2:
    st.metric("📈 Pertumbuhan Bulanan", f"{growth:.2f}%", delta=f"{current - previous:,.0f}")

# Visualisasi Total Penjualan per Bulan
monthly_sales = df.groupby('month')['total'].sum().reset_index()
fig1 = px.line(monthly_sales, x='month', y='total', markers=True, title='Total Penjualan per Bulan',
               labels={'month': 'Bulan', 'total': 'Total Penjualan (Rp)'},
               template='plotly_dark', color_discrete_sequence=['#00C49A'])
st.plotly_chart(fig1, use_container_width=True)

# Produk Terlaris
top_products = filtered_df.groupby('product_id')['quantity'].sum().sort_values(ascending=False).head(10).reset_index()
fig2 = px.bar(top_products, x='product_id', y='quantity', title='10 Produk Terlaris',
              labels={'product_id': 'Produk', 'quantity': 'Jumlah Terjual'},
              template='plotly_dark', color_discrete_sequence=['#66b3ff'])
st.plotly_chart(fig2, use_container_width=True)

# Penjualan per Lokasi
location_sales = filtered_df.groupby('customer_location')['total'].sum().sort_values(ascending=False).reset_index()
fig3 = px.bar(location_sales, x='customer_location', y='total', title='Total Penjualan per Lokasi',
              labels={'customer_location': 'Lokasi', 'total': 'Total Penjualan (Rp)'},
              template='plotly_dark', color_discrete_sequence=['#ffa07a'])
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")
st.caption("Dashboard ini dibangun dengan ❤️ menggunakan Streamlit dan Plotly.")
