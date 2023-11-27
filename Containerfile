FROM registry.access.redhat.com/ubi8/python-311:1-13

USER 1001

# Create directory for application resources
COPY --chown=1001 *.py /deployments/
COPY --chown=1001 requirements.txt /deployments/
COPY --chown=1001 datasets/ /deployments/datasets/
COPY --chown=1001 util/ /deployments/util/

WORKDIR /deployments

# Install dependencies
RUN pip install -r requirements.txt

# Configure container port and UID
EXPOSE 8080
USER 1001

# Run application
# CMD ["python", "/deployments/predict-async.py"]
CMD ["hypercorn", "--graceful-timeout", "5", "--bind", "0.0.0.0:8080", "predict-async:app"]