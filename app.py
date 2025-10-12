"""
Flask Web Application for MachineLearningStocks
Provides a full-stack interface for stock prediction and backtesting
Supports both US (S&P 500) and Indian (NIFTY 50) stock markets
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

# Configuration for market selection
# Set to 'INDIAN' for NIFTY 50 or 'US' for S&P 500
MARKET = os.environ.get('MARKET', 'INDIAN')  # Default to Indian market

# Market-specific configurations
MARKET_CONFIG = {
    'US': {
        'keystats_file': 'keystats.csv',
        'forward_file': 'forward_sample.csv',
        'index_name': 'S&P 500',
        'index_column': 'SP500_p_change',
        'currency': 'USD'
    },
    'INDIAN': {
        'keystats_file': 'indian_keystats.csv',
        'forward_file': 'indian_forward_sample.csv',
        'index_name': 'NIFTY 50',
        'index_column': 'NIFTY50_p_change',
        'currency': 'INR'
    }
}

# Get current market config
config = MARKET_CONFIG.get(MARKET, MARKET_CONFIG['INDIAN'])

# Global variables to cache models
cached_model = None
cached_data = None

# Optimized outperformance threshold for high precision (25% instead of 10%)
# This ensures we only predict stocks that significantly outperform the market
OUTPERFORMANCE = 25

# Minimum probability threshold for predictions (70% confidence required)
# This filters out low-confidence predictions and reduces false positives
MIN_PROBABILITY_THRESHOLD = 0.70


def load_data():
    """Load and cache the training data"""
    global cached_data
    if cached_data is None:
        keystats_file = config['keystats_file']
        if os.path.exists(keystats_file):
            cached_data = pd.read_csv(keystats_file)
            # Only drop rows where core columns are missing (not fundamental features)
            core_cols = ['Date', 'Unix', 'Ticker', 'Price', 'stock_p_change', config['index_column']]
            cached_data.dropna(subset=core_cols, inplace=True)
            # Set Date as index if it exists
            if 'Date' in cached_data.columns:
                cached_data = cached_data.set_index('Date')
        else:
            # Fallback to US data if Indian data not available
            cached_data = pd.read_csv("keystats.csv", index_col="Date")
            cached_data.dropna(axis=0, how="any", inplace=True)
    return cached_data


def train_model():
    """Train and cache the ML model"""
    global cached_model
    if cached_model is None:
        data = load_data()
        features = data.columns[6:]
        
        # Fill NaN values in features with 0
        data[features] = data[features].fillna(0)
        
        X_train = data[features].values
        
        # Use the appropriate index column based on market
        index_col = config['index_column']
        if index_col not in data.columns:
            index_col = 'SP500_p_change'  # Fallback
        
        y_train = list(
            status_calc(
                data["stock_p_change"],
                data[index_col],
                OUTPERFORMANCE,
            )
        )
        # Improved Random Forest with better hyperparameters for higher precision
        cached_model = RandomForestClassifier(
            n_estimators=200,  # More trees for better accuracy
            max_depth=10,  # Limit depth to prevent overfitting
            min_samples_split=20,  # Require more samples to split
            min_samples_leaf=10,  # Require more samples in leaf nodes
            max_features='sqrt',  # Use sqrt of features for each split
            class_weight='balanced',  # Handle class imbalance
            random_state=42
        )
        cached_model.fit(X_train, y_train)
    return cached_model


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html', 
                         market=MARKET, 
                         index_name=config['index_name'],
                         currency=config['currency'])


@app.route('/api/backtest', methods=['GET'])
def backtest():
    """Run backtesting and return results"""
    try:
        data = load_data()
        features = data.columns[6:]
        
        # Fill NaN values in features with 0
        data[features] = data[features].fillna(0)
        
        X = data[features].values
        
        # Use the appropriate index column based on market
        index_col = config['index_column']
        if index_col not in data.columns:
            index_col = 'SP500_p_change'  # Fallback
        
        y = list(
            status_calc(
                data["stock_p_change"], data[index_col], OUTPERFORMANCE
            )
        )
        z = np.array(data[["stock_p_change", index_col]])

        # Split the data with stratification to maintain class balance
        X_train, X_test, y_train, y_test, z_train, z_test = train_test_split(
            X, y, z, test_size=0.2, random_state=42, stratify=y
        )

        # Train improved model
        clf = RandomForestClassifier(
            n_estimators=200,
            max_depth=10,
            min_samples_split=20,
            min_samples_leaf=10,
            max_features='sqrt',
            class_weight='balanced',
            random_state=42
        )
        clf.fit(X_train, y_train)

        # Get probability predictions
        y_proba = clf.predict_proba(X_test)
        
        # Only predict stocks with high confidence (>60% probability)
        y_pred = np.zeros(len(y_test), dtype=int)
        y_pred[y_proba[:, 1] >= MIN_PROBABILITY_THRESHOLD] = 1
        
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
        forward_file = config['forward_file']
        if not os.path.exists(forward_file):
            forward_file = "forward_sample.csv"  # Fallback
        
        forward_data = pd.read_csv(forward_file)
        if "Date" in forward_data.columns:
            forward_data = forward_data.set_index("Date")
        
        # Only drop rows where Ticker is missing, keep rows with NaN features
        forward_data = forward_data[forward_data["Ticker"].notna()]
        
        # Get features from training data to match
        training_data = load_data()
        features = training_data.columns[6:]
        
        # Fill NaN values in features with 0 for prediction
        forward_data[features] = forward_data[features].fillna(0)
        
        X_test = forward_data[features].values
        tickers = forward_data["Ticker"].values

        # Get prediction probabilities first
        y_proba = model.predict_proba(X_test)
        
        # Only predict stocks with high confidence (>60% probability)
        y_pred = np.zeros(len(X_test), dtype=int)
        y_pred[y_proba[:, 1] >= MIN_PROBABILITY_THRESHOLD] = 1
        
        # Get predicted stocks
        predicted_stocks = tickers[y_pred == 1].tolist()
        
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
        forward_file = config['forward_file']
        if not os.path.exists(forward_file):
            forward_file = "forward_sample.csv"
        
        forward_data = pd.read_csv(forward_file)
        
        # Get date range info
        if hasattr(data.index, 'min'):
            date_start = str(data.index.min())
            date_end = str(data.index.max())
        elif 'Date' in data.columns:
            date_start = str(data['Date'].min())
            date_end = str(data['Date'].max())
        else:
            date_start = "N/A"
            date_end = "N/A"
        
        return jsonify({
            'training_samples': len(data),
            'forward_samples': len(forward_data),
            'features_count': len(data.columns) - 6,
            'date_range': {
                'start': date_start,
                'end': date_end
            },
            'market': MARKET,
            'index_name': config['index_name'],
            'currency': config['currency']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("Starting MachineLearningStocks Web Application...")
    print("Access the application at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
