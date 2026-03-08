FROM python:3.11-slim

# Install system dependencies required by Manim
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    libcairo2-dev \
    libpango1.0-dev \
    pkg-config \
    python3-dev \
    texlive-full \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
RUN pip install manim pydantic

WORKDIR /app

# Copy the worker script
COPY utils/worker.py worker.py

# Make the python script the entrypoint so we can pass arguments to it
ENTRYPOINT ["python", "worker.py"]