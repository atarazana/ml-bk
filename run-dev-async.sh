#!/bin/sh

export MODEL_PATH=./models/model.joblib

hypercorn --graceful-timeout 5 --bind localhost:8080 predict-async:app
