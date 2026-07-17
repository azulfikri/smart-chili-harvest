FROM python:3.10-slim

WORKDIR /app

# Install OS dependencies required by OpenCV / YOLOv8
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies list and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Use entrypoint to auto-init DB then start uvicorn
ENTRYPOINT ["./entrypoint.sh"]
