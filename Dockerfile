# Use Python 3.12 as base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy the entire code directory
COPY Code/ /app/Code/
COPY requirements.txt /app/
COPY data/ /app/data/

# Install dependencies using Pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Streamlit port
EXPOSE 8501

# Set the default command to run Streamlit
CMD ["streamlit", "run", "Code/vis.py"]