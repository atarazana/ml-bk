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

from util import CombinedAttributesAdder

app = Flask(__name__)
model = joblib.load('model.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    print(f'data={data}')
    input_data = pd.DataFrame(data, index=[0])
    print(input_data)
    prediction = model.predict(input_data).tolist()

    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True)
