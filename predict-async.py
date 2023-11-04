import sys
import os
import signal
import uuid

import joblib
import sklearn
import pandas as pd

import asyncio
from quart import Quart, request, jsonify

# Python ≥3.5 is required
assert sys.version_info >= (3, 5)

# Scikit-Learn ≥0.20 is required
assert sklearn.__version__ >= "0.20"

if "MODEL_PATH" in os.environ:
    pass
else:
    print("MODEL_PATH CANNOT BE EMPTY!!!")
    sys.exit()

MODEL_PATH = os.getenv("MODEL_PATH")

print(f"MODEL_PATH={MODEL_PATH}")


# Signals
def signal_handler(signal, frame):
    print("You pressed Ctrl+C!")
    print("Shutdown requested...exiting")

    sys.exit(0)


if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
    signal.signal(signal.SIGINT, signal_handler)

app = Quart(__name__)

model = joblib.load(MODEL_PATH)

predictions = {}


async def save_prediction(prediction_id, prediction_object):
    predictions[prediction_id] = prediction_object


async def run_prediction(prediction_id, payload):
    await save_prediction(prediction_id, {"status": "running", "predictionId": prediction_id})

    input_data = pd.DataFrame(payload, index=[0])
    print(input_data)
    prediction = model.predict(input_data).tolist()

    prediction_object = {
        "status": "success",
        "value": prediction,
        "valueType": "float",
        "explanation": "linear regressor value",
    }

    await save_prediction(prediction_id, prediction_object)
    return (prediction_id, prediction_object)


@app.route("/")
async def welcome():
    return "ml-bk api"


@app.route("/predict", methods=["POST"])
async def predict():
    print(f"request={request}")
    content_type = request.headers.get("Content-Type")
    print(f"content_type={content_type}")

    if content_type == "application/json":
        payload = await request.get_json()
        print(f"payload={payload}")

        # Calc prediction_id
        prediction_id = str(uuid.uuid4())
        # Run asynchronously... no wait
        asyncio.create_task(run_prediction(prediction_id, payload))

        return jsonify({"status": "running", "predictionId": prediction_id})
    else:
        response_data = {"status": "error", "explanation": "Content-Type not supported!"}
        return jsonify(response_data)


@app.route("/predictions/<predictionId>", methods=["GET"])
async def get_prediction(predictionId):
    print(f"predictionId={predictionId}")
    print(predictions)

    if predictionId in predictions:
        response_data = predictions[predictionId]
        return jsonify(response_data)

    response_data = {"status": "error", "explanation": "prediction not found"}
    return jsonify(response_data)


if __name__ == "__main__":
    app.run(debug=True)
