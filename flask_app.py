import sys
import time
import os
import signal
import uuid

from flask import Flask, request, jsonify

# if "MODEL_PATH" in os.environ:
#     pass
# else:
#     print('''MODEL_PATH CANNOT BE EMPTY!!!''')
#     sys.exit()


# MODEL_PATH = os.getenv('MODEL_PATH')

# print(f'MODEL_PATH={MODEL_PATH}')

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

# Flask
app = Flask(__name__)

# Init
predictions = {}
init()

def save_prediction(prediction_id, prediction_object):
    predictions[prediction_id] = prediction_object

def run_prediction(payload):
    prediction_id = uuid.uuid4()
    if 'firstName' in payload and 'lastName' in payload and 'email' in payload:
        prediction_object = {'status': 'success', 'value': '12.02', 'valueType': 'float', 'explanation': 'linear regressor value'}
    else:
        prediction_object = {'status': 'error', 'explanation': 'malformed parameters'}
    return (str(prediction_id), prediction_object)

@app.route('/')
def welcome():
    return 'ml-bk api'

@app.route('/predict',  methods = ['POST'])
def predict():
    print(f'request={request}')
    content_type = request.headers.get('Content-Type')
    print(f'content_type={content_type}')
    print(f'body={request.get_data(as_text=True)}')

    if (content_type == 'application/json'):
        payload = request.get_json()
        print(f'payload={payload}')
        
        (prediction_id, prediction_object) = run_prediction(payload)
        save_prediction(prediction_id, prediction_object)
        
        return jsonify({'status': 'running', 'predictionId': prediction_id})
    else:
        response_data = {'status': 'error', 'explanation': 'Content-Type not supported!'}
        return jsonify(response_data)

@app.route('/predictions/<predictionId>',  methods = ['GET'])
def get_prediction(predictionId):
    print(f'predictionId={predictionId}')
    print(predictions)
    
    if predictionId in predictions:
        response_data =  predictions[predictionId]
        return jsonify(response_data)

    response_data = {'status': 'error', 'explanation': 'prediction not found'}
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0')