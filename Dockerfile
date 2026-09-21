# Image de production Tharros : compile le front puis sert API + site avec uvicorn.
# Construction : docker build -t tharros .   |   Lancement : voir docker-compose.yml

# --- Étape 1 : front Vue compilé
FROM node:22-alpine AS front
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci --no-audit --no-fund
COPY frontend/ ./
RUN npm run build

# --- Étape 2 : API Python + fichiers statiques
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 ENVIRONMENT=production
WORKDIR /app
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt
COPY backend/ backend/
COPY --from=front /app/frontend/dist frontend/dist
RUN useradd -m tharros && mkdir -p backend/media && chown -R tharros:tharros /app
USER tharros
WORKDIR /app/backend
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips=*"]
