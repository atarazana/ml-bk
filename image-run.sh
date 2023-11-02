#!/bin/sh

. ./image-env.sh

# --entrypoint bash \

podman run -it --rm -p 5000:5000 \
  -e MODEL_PATH=/deployment/model.joblib \
  --volume kubeconfig:/var/kubeconfig \
  --user 1234 \
  --name bk localhost/${PROJECT_ID}:${VERSION}

