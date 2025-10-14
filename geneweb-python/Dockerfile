FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 2317

# Lancer la CLI gwd
CMD ["python", "-m", "geneweb.gwd"]
