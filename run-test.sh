#!/bin/sh

echo "This should predict a value close to: 244800.0"

curl http://localhost:5000/predictions/$(curl -sX POST -H "Content-Type: application/json" -d '{
    "longitude": -117.72,
    "latitude": 33.54,
    "housing_median_age": 13.0,
    "total_rooms": 4866.0,
    "total_bedrooms": 812.0,
    "population": 1909.0,
    "households": 733.0,
    "median_income": 4.9821,
    "ocean_proximity": "<1H OCEAN"
}' http://localhost:5000/predict | jq -r .predictionId)
