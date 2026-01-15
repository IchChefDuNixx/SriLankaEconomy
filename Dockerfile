# Use Python 3.12 as base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

COPY code/ /app/code/
COPY requirements.txt /app/
COPY data/ /app/data/

RUN pip install -r requirements.txt

EXPOSE 8501

# Set the default command to run Streamlit
CMD ["streamlit", "run", "code/Sri_Lankas_Journey.py"]
