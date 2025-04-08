FROM python:3.10-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


FROM python:3.10-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=core.settings

ENV POSTGRES_DB_NAME=dbname
ENV POSTGRES_USER=dbuser
ENV POSTGRES_PASS=dbpassword
ENV POSTGRES_HOST=dbhost
ENV POSTGRES_PORT=5432

ENV SECRET_KEY=sua-chave-secreta-aqui
ENV DEBUG=False
ENV ALLOWED_HOSTS=localhost,127.0.0.1,seu-dominio.com
ENV CSRF_TRUSTED_ORIGINS=http://localhost,https://seu-dominio.com

ENV EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
ENV EMAIL_HOST=smtp.example.com
ENV EMAIL_PORT=587
ENV EMAIL_HOST_USER=user@example.com
ENV EMAIL_HOST_PASSWORD=email_password
ENV EMAIL_USE_TLS=True

ENV TWILIO_ACCOUNT_SID=your_account_sid
ENV TWILIO_AUTH_TOKEN=your_auth_token
ENV TWILIO_PHONE_NUMBER=+1234567890

COPY . .

EXPOSE 8000

RUN sed -i 's/\r$//g' docker-entrypoint.sh
RUN chmod +x docker-entrypoint.sh 

ENTRYPOINT [ "sh", "docker-entrypoint.sh" ]
