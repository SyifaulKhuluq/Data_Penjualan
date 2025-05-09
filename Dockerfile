FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y build-essential && apt-get clean

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "dashboard_data_penjualan.py", "--server.port=8501", "--server.enableCORS=false"]
