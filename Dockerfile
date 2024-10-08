# Use the official Python image as the base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install --no-cache-dir virtualenv

RUN python -m venv /app/venv

COPY requirements.txt /app/
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt
COPY . /app/
EXPOSE 8000
CMD ["/app/venv/bin/gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "budidayaplus.wsgi:application"]