#!/bin/sh

export MODEL_PATH=./models/model.joblib

hypercorn --graceful-timeout 5 --bind localhost:5000 predict-async:app
