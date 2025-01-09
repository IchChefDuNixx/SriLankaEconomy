# Use Python 3.12 as base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy the entire code directory
COPY Code/ /app/Code/
COPY environment.yml /app/
COPY data/ /app/data/

# Install system dependencies required for Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install miniconda
RUN apt-get update && apt-get install -y wget && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh

# Add conda to path
ENV PATH="/opt/conda/bin:${PATH}"

# Create conda environment from yml file
RUN conda env create -f environment.yml

# Make RUN commands use the new environment
SHELL ["conda", "run", "-n", "vis24", "/bin/bash", "-c"]

# Expose the Streamlit port
EXPOSE 8501

# Set the default command to run Streamlit
CMD ["conda", "run", "-n", "vis24", "streamlit", "run", "Code/vis.py", "--server.address", "0.0.0.0"]