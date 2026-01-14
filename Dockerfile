# Use Python 3.10 slim as base
FROM python:3.10-slim

# Build arguments for security
ARG VNC_PASSWORD_ARG=coomerdl
ARG USER_ID=1000
ARG GROUP_ID=1000

# Prevent Python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
# - xvfb: Virtual Framebuffer for headless display
# - x11vnc: VNC server to expose the X11 display
# - fluxbox: Lightweight Window Manager
# - novnc & websockify: Web-based VNC viewer
# - ffmpeg: Required for media processing
# - chromium & firefox-esr: Browsers for Selenium/Playwright scrapers
# - tk: Tkinter support for the GUI
# - net-tools, procps: Utilities for supervision and debugging
RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb \
    x11vnc \
    fluxbox \
    novnc \
    websockify \
    ffmpeg \
    chromium \
    chromium-driver \
    firefox-esr \
    python3-tk \
    tk \
    curl \
    unzip \
    supervisor \
    net-tools \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set environment variables for Display and Cloud Run
ENV DISPLAY=:0 \
    RESOLUTION=1280x800x24 \
    PORT=8080 \
    VNC_PASSWORD=${VNC_PASSWORD_ARG}

# Expose ports
# 8080: Main entry (noVNC web interface, Cloud Run dynamic port)
# 5900: VNC server (direct VNC connection)
EXPOSE 8080 5900

# Copy configuration files
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY entrypoint.sh /app/entrypoint.sh

# Make entrypoint executable and create necessary directories
RUN chmod +x /app/entrypoint.sh && \
    mkdir -p /var/log/supervisor

# Health check to ensure services are running
# Note: Uses literal port 8080 as Docker HEALTHCHECK doesn't support variable expansion
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/vnc.html || exit 1

# Define entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
