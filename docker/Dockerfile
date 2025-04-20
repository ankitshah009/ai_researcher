FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including LaTeX
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    texlive-latex-base \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-latex-extra \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create directories for output and templates
RUN mkdir -p /app/outputs /app/templates

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Expose port
EXPOSE 5000

# Set command
CMD ["python", "api.py"] 