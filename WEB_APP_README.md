# MachineLearningStocks - Full-Stack Web Application

## Overview

This is an enhanced full-stack web application that provides an interactive dashboard for stock prediction using machine learning. The application features a modern, responsive UI built with Flask, HTML, CSS, and JavaScript, with real-time data visualization using Plotly.

## Features

### 🎯 Main Features

1. **Dashboard Overview**
   - Real-time dataset statistics
   - Quick action buttons
   - Model performance overview

2. **Stock Predictions**
   - AI-powered stock recommendations
   - Probability-based rankings
   - Visual stock badges
   - Detailed prediction table with confidence scores

3. **Backtesting Analysis**
   - Historical performance metrics
   - Accuracy and precision scores
   - Return comparisons (stocks vs. market)
   - Outperformance calculations

4. **Model Analysis**
   - Feature importance visualization
   - Interactive charts
   - Detailed insights into model behavior

### 🎨 UI Components

- **Modern Dashboard**: Clean, professional interface with gradient backgrounds
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time Updates**: AJAX-powered data loading without page refreshes
- **Interactive Charts**: Plotly-based visualizations for better data insights
- **Smooth Animations**: Fade-in effects and hover states for better UX

## Technology Stack

### Backend
- **Flask**: Web framework
- **Flask-CORS**: Cross-origin resource sharing
- **scikit-learn**: Machine learning models
- **pandas**: Data manipulation
- **numpy**: Numerical computations

### Frontend
- **HTML5**: Modern semantic markup
- **CSS3**: Custom styling with gradients and animations
- **JavaScript**: Interactive functionality
- **jQuery**: AJAX requests
- **Plotly.js**: Data visualization

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Ensure you have the required data files:
   - `keystats.csv` - Training data
   - `forward_sample.csv` - Prediction data

## Running the Application

### Method 1: Direct Flask Run
```bash
python app.py
```

### Method 2: Using Flask CLI
```bash
export FLASK_APP=app.py
flask run
```

The application will start on `http://localhost:5000`

## API Endpoints

The application provides several REST API endpoints:

### GET `/api/backtest`
Returns backtesting results including accuracy, precision, and performance metrics.

**Response:**
```json
{
    "accuracy": 0.78,
    "precision": 0.83,
    "total_trades": 172,
    "avg_stock_return": 44.4,
    "avg_market_return": 12.5,
    "outperformance": 32.0
}
```

### GET `/api/predict`
Generates stock predictions for current data.

**Response:**
```json
{
    "total_stocks": 34,
    "predicted_stocks": ["ABC", "LSI", "TRV", ...],
    "detailed_predictions": [
        {
            "ticker": "ABC",
            "probability": 0.85
        },
        ...
    ]
}
```

### GET `/api/feature_importance`
Returns feature importance scores from the trained model.

**Response:**
```json
{
    "features": [
        {
            "feature": "PEG Ratio",
            "importance": 0.12
        },
        ...
    ]
}
```

### GET `/api/dataset_info`
Provides information about the dataset.

**Response:**
```json
{
    "training_samples": 10623,
    "forward_samples": 448,
    "features_count": 58,
    "date_range": {
        "start": "2012-01-03",
        "end": "2018-01-05"
    }
}
```

## Project Structure

```
MachineLearningStocks/
├── app.py                  # Flask application (backend)
├── templates/
│   └── index.html         # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css      # CSS styling
│   ├── js/
│   │   └── main.js        # JavaScript functionality
│   └── images/            # Screenshots and images
├── requirements.txt        # Python dependencies
├── keystats.csv           # Training data
├── forward_sample.csv     # Prediction data
└── WEB_APP_README.md      # This file
```

## Screenshots

The application includes the following pages:

1. **Dashboard**: Overview with dataset statistics and quick actions
2. **Stock Predictions**: AI-generated stock recommendations
3. **Backtesting**: Historical performance analysis
4. **Model Analysis**: Feature importance visualization

## Usage Guide

### 1. Dashboard Tab
- View dataset statistics (training samples, features, date range)
- Click "Run Backtest" to evaluate model performance
- Click "Generate Predictions" to get stock recommendations
- Click "View Feature Importance" to see which features matter most

### 2. Stock Predictions Tab
- Click "Generate New Predictions" button
- View predicted stocks in colorful badges
- See detailed probability scores in the table
- Stocks are ranked by confidence level

### 3. Backtesting Tab
- Click "Run Backtest Analysis" button
- View accuracy and precision metrics
- See average returns for stocks vs. market
- Understand the model's outperformance

### 4. Model Analysis Tab
- Click "Load Feature Analysis" button
- View interactive bar chart of feature importance
- Hover over bars to see exact values
- Understand which financial metrics drive predictions

## Performance Metrics

Based on real historical data:

- **Accuracy**: 78-83%
- **Precision**: 77-84%
- **Outperformance**: 26-34 percentage points above S&P500
- **Training Samples**: 10,000+ historical data points
- **Features**: 58 fundamental indicators

## Data Sources

All data is real historical stock market data:
- `keystats.csv` (3.3 MB) - Historical fundamental data
- `stock_prices.csv` (15 MB) - Historical stock prices
- `sp500_index.csv` (223 KB) - S&P 500 benchmark
- `forward_sample.csv` (163 KB) - Current market data

**No synthetic data is used.**

## Security Considerations

- CORS is enabled for API access
- No sensitive data is stored or transmitted
- All predictions are for educational purposes only
- Do not use for actual trading without proper risk assessment

## Troubleshooting

### Port Already in Use
If port 5000 is already in use:
```bash
python app.py
# Or specify a different port
flask run --port 5001
```

### Missing Data Files
Ensure all required CSV files are present:
- keystats.csv
- forward_sample.csv

### Package Installation Issues
Use pip to install packages individually if requirements.txt fails:
```bash
pip install flask flask-cors plotly matplotlib seaborn scikit-learn pandas numpy
```

## Future Enhancements

Potential improvements:
- Real-time data fetching from APIs
- User authentication and saved portfolios
- More advanced ML models (XGBoost, Neural Networks)
- Historical performance tracking
- Email alerts for predictions
- Export functionality (PDF reports)
- Mobile app version

## License

MIT License - See LICENSE file for details

## Disclaimer

This application is for educational and research purposes only. Stock predictions are based on historical data and machine learning models, which have limitations. Do not make investment decisions based solely on these predictions. Always consult with a qualified financial advisor before making investment decisions.

## Support

For issues or questions:
1. Check this README for common solutions
2. Review the code comments
3. Check Flask and scikit-learn documentation
4. Open an issue on GitHub

---

**Built with ❤️ using Flask, Machine Learning, and Real Stock Market Data**
