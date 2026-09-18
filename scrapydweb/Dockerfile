FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir scrapydweb==1.6.0

COPY scrapydweb_settings_v11.py .

EXPOSE 5000

CMD ["scrapydweb"]
