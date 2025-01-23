FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    iputils-ping \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libnss3 \
    libxrandr2 \
    libasound2 \
    libpango1.0-0 \
    libcups2 \
    libxss1 \
    libxshmfence1 \
    libgbm1 \
    && rm -rf /var/lib/apt/lists/*

COPY google-chrome-stable_114.0.5735.90-1_amd64.deb /tmp/
RUN dpkg -i /tmp/google-chrome-stable_114.0.5735.90-1_amd64.deb || true \
    && apt-get install -f -y \
    && rm /tmp/google-chrome-stable_114.0.5735.90-1_amd64.deb

RUN echo "deb http://apt.postgresql.org/pub/repos/apt bookworm-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
    && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && apt-get update \
    && apt-get install -y postgresql-client-16 \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver_linux64.zip

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn

COPY . /app/

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "final_project.wsgi:application"]
