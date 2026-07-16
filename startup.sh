#!/bin/bash
apt-get update
apt-get install -y unixodbc-dev
apt-get install -y msodbcsql18
pip install -r requirements.txt
gunicorn --bind=0.0.0.0:8000 app:app

