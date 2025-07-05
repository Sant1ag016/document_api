# Use Python 3.9-slim as the base image
FROM python:3.9-slim

# Set working directory in the container
WORKDIR /app

# Install only the dependencies required for Tesseract and PIL
RUN apt-get update && \
    apt-get install -y tesseract-ocr libglib2.0-0 libsm6 libxext6 libxrender-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy the application files into the container
COPY . /app/

# Install required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port for FastAPI (by default, FastAPI runs on port 8000)
EXPOSE 8000

# Command to run FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
