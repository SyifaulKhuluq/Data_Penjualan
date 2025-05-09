# Gunakan base image Python yang ringan
FROM python:3.10-slim

# Install dependensi dasar sistem (opsional tapi disarankan)
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean

# Set direktori kerja di dalam container
WORKDIR /app

# Salin semua file dari direktori lokal ke dalam container
COPY . .

# Install dependensi dari requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Buka port default Streamlit
EXPOSE 8501

# Jalankan aplikasi Streamlit
CMD ["streamlit", "run", “dashboard_data_penjualan.py, "--server.port=8501", "--server.enableCORS=false"]
