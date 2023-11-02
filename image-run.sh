#!/bin/sh

. ./image-env.sh

# --entrypoint bash \

podman run -it --rm -p 6000:5000 \
  -e MODEL_PATH=/models/model.joblib \
  --volume $(pwd)/models:/models:z \
  --user 1234 \
  --name bk localhost/${PROJECT_ID}:${VERSION}