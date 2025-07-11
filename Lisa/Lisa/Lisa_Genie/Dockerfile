FROM python:3.12-slim

# Dossier de travail dans le container
WORKDIR /app

# Copie les fichiers du dossier courant vers /app dans le container
COPY . /app

# Installe les dépendances Python nécessaires
RUN pip install flask flask-cors gunicorn

# Expose le port 5000 du container
EXPOSE 5000

# Lance ton application Flask avec Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "BirdFeedbackAPI:app"]
