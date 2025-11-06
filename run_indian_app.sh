#!/bin/bash
# Script to run the Flask app with Indian market configuration

cd /home/runner/work/MachineLearningStocks/MachineLearningStocks
export MARKET=INDIAN
echo "Starting MachineLearningStocks with Indian Market (NIFTY 50)..."
echo "Access the application at: http://localhost:5000"
python app.py
