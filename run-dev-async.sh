#!/bin/sh

hypercorn --graceful-timeout 5 --bind localhost:5000 predict-async:app
