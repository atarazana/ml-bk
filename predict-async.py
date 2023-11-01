import sys
import time
import os
import signal
import uuid

# Signals
def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    print('Shutdown requested...exiting')
   
    sys.exit(0)

if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
    signal.signal(signal.SIGINT, signal_handler)

# Init
def init ():
    print('Init hook!')

from flask import Flask, request, jsonify
import joblib

# Python ≥3.5 is required
import sys
assert sys.version_info >= (3, 5)

# Scikit-Learn ≥0.20 is required
import sklearn
assert sklearn.__version__ >= "0.20"

# Common imports
import numpy as np
import os

import pandas as pd

from sklearn.datasets import load_iris
from sklearn.model_selection import StratifiedShuffleSplit

from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression

rooms_ix, bedrooms_ix, population_ix, households_ix = 3, 4, 5, 6

class CombinedAttributesAdder(BaseEstimator, TransformerMixin):
    def __init__(self, add_bedrooms_per_room=True): # no *args or **kargs
        self.add_bedrooms_per_room = add_bedrooms_per_room
    def fit(self, X, y=None):
        return self  # nothing else to do
    def transform(self, X):
        rooms_per_household = X[:, rooms_ix] / X[:, households_ix]
        population_per_household = X[:, population_ix] / X[:, households_ix]
        if self.add_bedrooms_per_room:
            bedrooms_per_room = X[:, bedrooms_ix] / X[:, rooms_ix]
            return np.c_[X, rooms_per_household, population_per_household,
                         bedrooms_per_room]
        else:
            return np.c_[X, rooms_per_household, population_per_household]

import uuid
from quart import Quart, request, jsonify
import hypercorn
import asyncio

# app = Flask(__name__)
app = Quart(__name__)

model = joblib.load('model.joblib')

predictions = {}

async def save_prediction(prediction_id, prediction_object):
    predictions[prediction_id] = prediction_object

async def run_prediction_dummmy(prediction_id, payload):
    await save_prediction(prediction_id, {'status': 'running', 'predictionId': prediction_id})
    await asyncio.sleep(5)  # Simulate a long-running task
    
    input_data = pd.DataFrame(payload, index=[0])
    prediction = model.predict(input_data).tolist()

    prediction_object = {'status': 'success', 'value': prediction, 'valueType': 'float', 'explanation': 'linear regressor value'}

    # if 'firstName' in payload and 'lastName' in payload and 'email' in payload:
    #     prediction_object = {'status': 'success', 'value': '12.02', 'valueType': 'float', 'explanation': 'linear regressor value'}
    # else:
    #     prediction_object = {'status': 'error', 'explanation': 'malformed parameters'}

    await save_prediction(prediction_id, prediction_object)
    return (prediction_id, prediction_object)

async def run_prediction(prediction_id, payload):
    await save_prediction(prediction_id, {'status': 'running', 'predictionId': prediction_id})

    print('>>>>>>>>')
    input_data = pd.DataFrame(payload, index=[0])
    print(input_data)
    prediction = model.predict(input_data).tolist()
    
    # df = pd.DataFrame([5.1, 3.5, 1.5, 1.2])
    # prediction = model.predict([[5.1, 3.5, 1.5, 1.2]])
    print('<<<<<<<<')

    # if 'firstName' in payload and 'lastName' in payload and 'email' in payload:
    #     prediction_object = {'status': 'success', 'value': '12.02', 'valueType': 'float', 'explanation': 'linear regressor value'}
    # else:
    #     prediction_object = {'status': 'error', 'explanation': 'malformed parameters'}

    prediction_object = {'status': 'success', 'value': prediction, 'valueType': 'float', 'explanation': 'linear regressor value'}

    await save_prediction(prediction_id, prediction_object)
    return (prediction_id, prediction_object)

@app.route('/')
async def welcome():
    return 'ml-bk api'

# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.get_json()
#     print(f'data={data}')
#     input_data = pd.DataFrame(data, index=[0])
#     print(input_data)
#     prediction = model.predict(input_data).tolist()

#     return jsonify({'prediction': prediction})

@app.route('/predict',  methods = ['POST'])
async def predict():
    print(f'request={request}')
    content_type = request.headers.get('Content-Type')
    print(f'content_type={content_type}')
    body = await request.get_data()

    if (content_type == 'application/json'):
        payload = await request.get_json()
        print(f'payload={payload}')

        # Calc prediction_id
        prediction_id = str(uuid.uuid4())
        # Run asyncronously... no wait
        print('create_task 1')
        # input_data = pd.DataFrame(payload, index=[0])
        # prediction = model.predict(input_data).tolist()
        asyncio.create_task(run_prediction(prediction_id, payload))
        print('create_task 2')
        # (prediction_id, prediction_object) = await run_prediction(prediction_id, payload)
        # await save_prediction(prediction_id, prediction_object)

        return jsonify({'status': 'running', 'predictionId': prediction_id})
    else:
        response_data = {'status': 'error', 'explanation': 'Content-Type not supported!'}
        return jsonify(response_data)

@app.route('/predictions/<predictionId>',  methods = ['GET'])
async def get_prediction(predictionId):
    print(f'predictionId={predictionId}')
    print(predictions)

    if predictionId in predictions:
        response_data =  predictions[predictionId]
        return jsonify(response_data)

    response_data = {'status': 'error', 'explanation': 'prediction not found'}
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
