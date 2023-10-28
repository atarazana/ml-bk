import sys
import time
import os
import signal

from flask import Flask, request

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

init()
       
@app.route('/')
def welcome():
    return 'ml-bk api'

@app.route('/predict',  methods = ['POST'])
def predict():
    print(f'request={request}')
    content_type = request.headers.get('Content-Type')
    print(f'content_type={content_type}')
    if (content_type == 'application/json'):
        payload = request.get_json()
        print(f'payload={payload}')
        if 'firstName' in payload and 'lastName' in payload and 'email' in payload:
            
            response_data = {'status': 'success', 'message': 'JSON data received successfully'}
            return jsonify(response_data)
        
        return 'ERROR'
    else:
        return 'Content-Type not supported!'

if __name__ == '__main__':
    app.run(host='0.0.0.0')