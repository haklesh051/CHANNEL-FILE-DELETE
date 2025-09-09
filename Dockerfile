# Latest stable Python slim image use karo (buster hatao)
FROM python:3.10-slim

# System dependencies install karo
RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends gcc libffi-dev musl-dev ffmpeg aria2 python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# App files copy karo
COPY . /app/
WORKDIR /app/

# Python dependencies install karo
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt
RUN pip install --no-cache-dir pytube

# Env variable
ENV COOKIES_FILE_PATH="youtube_cookies.txt"

# App start command
CMD gunicorn app:app & python3 main.py
