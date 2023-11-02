#!/bin/sh

# python app.py
gunicorn --workers=1 --graceful-timeout 5 --bind localhost:5000 predict:app