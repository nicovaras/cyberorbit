FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn
COPY . .
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
ENV FLASK_APP=app.py
