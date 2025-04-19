FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    texlive-latex-base \
    texlive-fonts-recommended \
    texlive-latex-extra \
    build-essential \
    curl \
    ffmpeg \
    git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create directories for output and templates
RUN mkdir -p /app/outputs /app/templates && \
    chown -R appuser:appuser /app

# Copy application code
COPY . .

# Change ownership of files
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Create volume for outputs and env file
VOLUME ["/app/outputs", "/app/.env"]

# Expose port for web UI
EXPOSE 7860

# Add health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:7860/ || exit 1

# Default entrypoint
ENTRYPOINT ["python"]

# Default command (can be overridden by docker run)
CMD ["main.py", "--topic", "Deep Learning"] 