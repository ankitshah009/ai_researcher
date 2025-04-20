FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install essential packages AND LaTeX for PDF generation
# Using texlive-full for simplicity, consider smaller subsets for optimization
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    texlive-full \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install -r requirements.txt

# Create output directory
RUN mkdir -p /app/outputs

# Copy source code
COPY . .

# Set environment
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

EXPOSE 5000
CMD ["python", "api.py"]