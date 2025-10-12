"""
Flask Web Application for MachineLearningStocks
Provides a full-stack interface for stock prediction and backtesting
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, accuracy_score
from utils import status_calc
import plotly.graph_objs as go
import plotly.utils
import json
import os

app = Flask(__name__)
CORS(app)

# Global variables to cache models
cached_model = None
cached_data = None

OUTPERFORMANCE = 10


def load_data():
    """Load and cache the training data"""
    global cached_data
    if cached_data is None:
        cached_data = pd.read_csv("keystats.csv", index_col="Date")
        cached_data.dropna(axis=0, how="any", inplace=True)
    return cached_data


def train_model():
    """Train and cache the ML model"""
    global cached_model
    if cached_model is None:
        data = load_data()
        features = data.columns[6:]
        X_train = data[features].values
        y_train = list(
            status_calc(
                data["stock_p_change"],
                data["SP500_p_change"],
                OUTPERFORMANCE,
            )
        )
        cached_model = RandomForestClassifier(n_estimators=100, random_state=0)
        cached_model.fit(X_train, y_train)
    return cached_model


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')


@app.route('/api/backtest', methods=['GET'])
def backtest():
    """Run backtesting and return results"""
    try:
        data = load_data()
        features = data.columns[6:]
        X = data[features].values
        y = list(
            status_calc(
                data["stock_p_change"], data["SP500_p_change"], OUTPERFORMANCE
            )
        )
        z = np.array(data[["stock_p_change", "SP500_p_change"]])

        # Split the data
        X_train, X_test, y_train, y_test, z_train, z_test = train_test_split(
            X, y, z, test_size=0.2, random_state=42
        )

        # Train model
        clf = RandomForestClassifier(n_estimators=100, random_state=0)
        clf.fit(X_train, y_train)

        # Predictions
        y_pred = clf.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)

        # Calculate returns
        stock_returns = []
        market_returns = []
        for i in range(len(y_pred)):
            if y_pred[i] == 1:
                stock_returns.append((z_test[i][0] / 100) + 1)
                market_returns.append((z_test[i][1] / 100) + 1)

        num_positive_predictions = len(stock_returns)
        if num_positive_predictions > 0:
            avg_stock_return = (sum(stock_returns) / num_positive_predictions - 1) * 100
            avg_market_return = (sum(market_returns) / num_positive_predictions - 1) * 100
            outperformance = avg_stock_return - avg_market_return
        else:
            avg_stock_return = 0
            avg_market_return = 0
            outperformance = 0

        return jsonify({
            'accuracy': float(accuracy),
            'precision': float(precision),
            'total_trades': num_positive_predictions,
            'avg_stock_return': float(avg_stock_return),
            'avg_market_return': float(avg_market_return),
            'outperformance': float(outperformance)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict', methods=['GET'])
def predict():
    """Generate stock predictions"""
    try:
        # Train model
        model = train_model()
        
        # Load forward data
        forward_data = pd.read_csv("forward_sample.csv", index_col="Date")
        forward_data.dropna(axis=0, how="any", inplace=True)
        features = forward_data.columns[6:]
        X_test = forward_data[features].values
        tickers = forward_data["Ticker"].values

        # Get predictions
        y_pred = model.predict(X_test)
        
        # Get predicted stocks
        predicted_stocks = tickers[y_pred == 1].tolist()
        
        # Get prediction probabilities
        y_proba = model.predict_proba(X_test)
        
        # Create detailed predictions
        predictions = []
        for i, ticker in enumerate(tickers):
            if y_pred[i] == 1:
                predictions.append({
                    'ticker': ticker,
                    'probability': float(y_proba[i][1])
                })
        
        # Sort by probability
        predictions.sort(key=lambda x: x['probability'], reverse=True)
        
        return jsonify({
            'total_stocks': len(predicted_stocks),
            'predicted_stocks': predicted_stocks,
            'detailed_predictions': predictions
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/feature_importance', methods=['GET'])
def feature_importance():
    """Get feature importance from the trained model"""
    try:
        model = train_model()
        data = load_data()
        features = data.columns[6:]
        
        importances = model.feature_importances_
        
        # Create feature importance list
        feature_list = []
        for i, feature in enumerate(features):
            feature_list.append({
                'feature': feature,
                'importance': float(importances[i])
            })
        
        # Sort by importance
        feature_list.sort(key=lambda x: x['importance'], reverse=True)
        
        # Take top 15 features
        top_features = feature_list[:15]
        
        return jsonify({
            'features': top_features
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/dataset_info', methods=['GET'])
def dataset_info():
    """Get information about the dataset"""
    try:
        data = load_data()
        forward_data = pd.read_csv("forward_sample.csv", index_col="Date")
        
        return jsonify({
            'training_samples': len(data),
            'forward_samples': len(forward_data),
            'features_count': len(data.columns) - 6,
            'date_range': {
                'start': str(data.index.min()),
                'end': str(data.index.max())
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("Starting MachineLearningStocks Web Application...")
    print("Access the application at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
