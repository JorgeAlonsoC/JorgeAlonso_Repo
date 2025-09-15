# ===== Base =====
FROM python:3.11-slim

# Config Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# (Opcional) instala certs y utilidades mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Workdir
WORKDIR /app

# Dependencias
# Asegúrate de tener un requirements.txt SIN 'python' (solo libs)
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install -r requirements.txt \
 && pip install gunicorn

# Código
COPY . .

# Usuario no-root
RUN useradd -m appuser
USER appuser

# Puerto
EXPOSE 8000

# Variables de entorno (ajusta/inyecta en runtime)
# Ejemplo: docker run -e GROQ_API_KEY=tu_api_key ...
ENV GROQ_API_KEY=""

# Arranque con Gunicorn
# Cambia 'app:app' si tu módulo/variable WSGI es distinto (p.ej. wsgi:app)
CMD ["gunicorn", "-w", "2", "-k", "gthread", "-b", "0.0.0.0:8000", "app:app"]
