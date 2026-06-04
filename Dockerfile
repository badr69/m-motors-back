# Image Python
FROM python:3.11-slim

# Dossier de travail dans le container
WORKDIR /app

# Copier requirements
COPY requirements.txt .

# Installer dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le projet backend
COPY . .

# Port Flask
EXPOSE 5000

# Lancer l'application avec Gunicorn
CMD ["gunicorn", "run:app", "-b", "0.0.0.0:5000"]
