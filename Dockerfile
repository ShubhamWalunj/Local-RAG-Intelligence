# 1. Use a stable Python base image
FROM python:3.10-slim

# 2. Set the working directory
WORKDIR /app

# 3. Install ONLY the essential build tools for ChromaDB
# We removed software-properties-common as it's not required for this stack.
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the project
COPY . .

# 6. Expose Streamlit port
EXPOSE 8501

# 7. Start command
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]