// Main JavaScript for MachineLearningStocks Web Application

// Tab switching functionality
function showTab(tabName) {
    // Hide all tab contents
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(tab => tab.classList.remove('active'));
    
    // Remove active class from all nav tabs
    const navTabs = document.querySelectorAll('.nav-tab');
    navTabs.forEach(tab => tab.classList.remove('active'));
    
    // Show selected tab
    document.getElementById(tabName).classList.add('active');
    
    // Add active class to clicked nav tab
    event.target.classList.add('active');
}

// Load dataset information on page load
document.addEventListener('DOMContentLoaded', function() {
    loadDatasetInfo();
});

// Helper function for fetch with error handling
function fetchAPI(url) {
    return fetch(url).then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    });
}

// Load dataset information
function loadDatasetInfo() {
    fetchAPI('/api/dataset_info')
        .then(data => {
            document.getElementById('training-samples').textContent = data.training_samples.toLocaleString();
            document.getElementById('forward-samples').textContent = data.forward_samples.toLocaleString();
            document.getElementById('features-count').textContent = data.features_count;
            document.getElementById('date-range').textContent = `${data.date_range.start} to ${data.date_range.end}`;
            document.getElementById('status').textContent = 'Active';
            document.getElementById('status').style.color = '#10b981';
            
            // Update market info
            const marketInfo = `${data.market} Market | ${data.index_name} | Currency: ${data.currency}`;
            document.getElementById('market-info').textContent = marketInfo;
        })
        .catch(error => {
            console.error('Error loading dataset info:', error);
            document.getElementById('status').textContent = 'Error';
            document.getElementById('status').style.color = '#ef4444';
        });
}

// Run backtesting
function runBacktest() {
    const resultsDiv = document.getElementById('backtest-results');
    const loadingDiv = document.getElementById('backtest-loading');
    const overviewDiv = document.getElementById('overview-message');
    
    // Show loading
    loadingDiv.style.display = 'block';
    resultsDiv.innerHTML = '';
    
    fetchAPI('/api/backtest')
        .then(data => {
            loadingDiv.style.display = 'none';
            
            if (data.error) {
                resultsDiv.innerHTML = `<div class="alert alert-error">Error: ${data.error}</div>`;
                return;
            }
            
            // Create results display
            const resultsHTML = `
                <div class="alert alert-success fade-in">
                    ✅ Backtest completed successfully!
                </div>
                
                <div class="results-grid fade-in">
                    <div class="result-card">
                        <h3>Accuracy Score</h3>
                        <div class="result-value">${(data.accuracy * 100).toFixed(1)}%</div>
                    </div>
                    <div class="result-card">
                        <h3>Precision Score</h3>
                        <div class="result-value">${(data.precision * 100).toFixed(1)}%</div>
                    </div>
                    <div class="result-card">
                        <h3>Total Trades</h3>
                        <div class="result-value">${data.total_trades}</div>
                    </div>
                    <div class="result-card">
                        <h3>Avg Stock Return</h3>
                        <div class="result-value">${data.avg_stock_return.toFixed(1)}%</div>
                    </div>
                    <div class="result-card">
                        <h3>Avg Market Return</h3>
                        <div class="result-value">${data.avg_market_return.toFixed(1)}%</div>
                    </div>
                    <div class="result-card">
                        <h3>Outperformance</h3>
                        <div class="result-value" style="color: #10b981;">+${data.outperformance.toFixed(1)}%</div>
                    </div>
                </div>
                
                <div style="margin-top: 30px; padding: 20px; background: #f0fdf4; border-radius: 10px; border: 2px solid #86efac;">
                    <h3 style="color: #166534; margin-bottom: 10px;">📊 Performance Summary</h3>
                    <p style="color: #166534;">
                        The ML model achieved <strong>${(data.accuracy * 100).toFixed(1)}%</strong> accuracy with 
                        <strong>${(data.precision * 100).toFixed(1)}%</strong> precision. Based on <strong>${data.total_trades}</strong> 
                        trades, the strategy generated an average return of <strong>${data.avg_stock_return.toFixed(1)}%</strong> 
                        compared to the market's <strong>${data.avg_market_return.toFixed(1)}%</strong>, 
                        resulting in an outperformance of <strong>${data.outperformance.toFixed(1)} percentage points</strong>.
                    </p>
                </div>
            `;
            
            resultsDiv.innerHTML = resultsHTML;
            
            // Update overview in dashboard
            if (overviewDiv) {
                overviewDiv.innerHTML = `
                    <div class="results-grid fade-in">
                        <div class="result-card">
                            <h3>Model Accuracy</h3>
                            <div class="result-value">${(data.accuracy * 100).toFixed(1)}%</div>
                        </div>
                        <div class="result-card">
                            <h3>Strategy Outperformance</h3>
                            <div class="result-value" style="color: #10b981;">+${data.outperformance.toFixed(1)}%</div>
                        </div>
                    </div>
                `;
            }
        })
        .catch(error => {
            loadingDiv.style.display = 'none';
            resultsDiv.innerHTML = `<div class="alert alert-error">Error running backtest: ${error.message}</div>`;
            console.error('Error:', error);
        });
}

// Generate predictions
function generatePredictions() {
    const resultsDiv = document.getElementById('predictions-results');
    const loadingDiv = document.getElementById('predictions-loading');
    
    // Show loading
    loadingDiv.style.display = 'block';
    resultsDiv.innerHTML = '';
    
    fetchAPI('/api/predict')
        .then(data => {
            loadingDiv.style.display = 'none';
            
            if (data.error) {
                resultsDiv.innerHTML = `<div class="alert alert-error">Error: ${data.error}</div>`;
                return;
            }
            
            if (data.total_stocks === 0) {
                resultsDiv.innerHTML = `
                    <div class="alert alert-info">
                        No stocks predicted to outperform the market by more than 10% at this time.
                    </div>
                `;
                return;
            }
            
            // Create stock badges
            let stockBadgesHTML = '<div class="stock-grid fade-in">';
            data.predicted_stocks.forEach(stock => {
                stockBadgesHTML += `<div class="stock-badge">${stock}</div>`;
            });
            stockBadgesHTML += '</div>';
            
            // Create detailed table
            let tableHTML = `
                <div class="stock-details fade-in">
                    <h3>Detailed Predictions (Top Picks by Probability)</h3>
                    <table class="stock-table">
                        <thead>
                            <tr>
                                <th>Rank</th>
                                <th>Ticker</th>
                                <th>Confidence</th>
                                <th>Probability</th>
                            </tr>
                        </thead>
                        <tbody>
            `;
            
            data.detailed_predictions.forEach((pred, index) => {
                const confidence = pred.probability >= 0.7 ? 'High' : pred.probability >= 0.6 ? 'Medium' : 'Low';
                tableHTML += `
                    <tr>
                        <td><strong>#${index + 1}</strong></td>
                        <td><strong style="color: #2563eb;">${pred.ticker}</strong></td>
                        <td>${confidence}</td>
                        <td>
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <div class="probability-bar" style="flex: 1;">
                                    <div class="probability-fill" style="width: ${pred.probability * 100}%"></div>
                                </div>
                                <span>${(pred.probability * 100).toFixed(1)}%</span>
                            </div>
                        </td>
                    </tr>
                `;
            });
            
            tableHTML += `
                        </tbody>
                    </table>
                </div>
            `;
            
            const resultsHTML = `
                <div class="alert alert-success fade-in">
                    ✅ Generated predictions for ${data.total_stocks} stocks!
                </div>
                
                <div style="margin: 20px 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;">
                    <h3 style="margin-bottom: 10px;">🎯 Predicted to Outperform S&P500</h3>
                    <p style="font-size: 1.1em;">
                        The ML model identified <strong>${data.total_stocks} stocks</strong> 
                        predicted to outperform the S&P500 index by more than 10%.
                    </p>
                </div>
                
                ${stockBadgesHTML}
                ${tableHTML}
            `;
            
            resultsDiv.innerHTML = resultsHTML;
        })
        .catch(error => {
            loadingDiv.style.display = 'none';
            resultsDiv.innerHTML = `<div class="alert alert-error">Error generating predictions: ${error.message}</div>`;
            console.error('Error:', error);
        });
}

// Load feature importance
function loadFeatureImportance() {
    const chartDiv = document.getElementById('feature-chart');
    const loadingDiv = document.getElementById('analysis-loading');
    const messageDiv = document.getElementById('analysis-message');
    
    // Show loading
    loadingDiv.style.display = 'block';
    messageDiv.style.display = 'none';
    chartDiv.innerHTML = '';
    
    fetchAPI('/api/feature_importance')
        .then(data => {
            loadingDiv.style.display = 'none';
            
            if (data.error) {
                messageDiv.innerHTML = `<div class="alert alert-error">Error: ${data.error}</div>`;
                messageDiv.style.display = 'block';
                return;
            }
            
            // Create HTML table for feature importance
            let tableHTML = `
                <div class="alert alert-success fade-in">
                    ✅ Feature analysis completed successfully!
                </div>
                
                <div style="margin-top: 20px;">
                    <h3>Top 15 Most Important Features</h3>
                    <table class="stock-table">
                        <thead>
                            <tr>
                                <th>Rank</th>
                                <th>Feature</th>
                                <th>Importance Score</th>
                                <th>Visual</th>
                            </tr>
                        </thead>
                        <tbody>
            `;
            
            data.features.forEach((feature, index) => {
                const percentage = (feature.importance * 100).toFixed(2);
                tableHTML += `
                    <tr>
                        <td><strong>#${index + 1}</strong></td>
                        <td><strong style="color: #2563eb;">${feature.feature}</strong></td>
                        <td>${percentage}%</td>
                        <td>
                            <div class="probability-bar" style="width: 200px;">
                                <div class="probability-fill" style="width: ${percentage}%"></div>
                            </div>
                        </td>
                    </tr>
                `;
            });
            
            tableHTML += `
                        </tbody>
                    </table>
                </div>
                
                <div class="alert alert-info fade-in" style="margin-top: 20px;">
                    <h4>📊 Feature Importance Analysis</h4>
                    <p style="margin-top: 10px;">
                        The table above shows the top 15 features that contribute most to the model's predictions.
                        Higher importance scores indicate features that have more influence on determining whether a stock 
                        will outperform the market. The Random Forest model uses these features to make intelligent
                        predictions about stock performance.
                    </p>
                </div>
            `;
            
            chartDiv.innerHTML = tableHTML;
        })
        .catch(error => {
            loadingDiv.style.display = 'none';
            messageDiv.innerHTML = `<div class="alert alert-error">Error loading feature importance: ${error.message}</div>`;
            messageDiv.style.display = 'block';
            console.error('Error:', error);
        });
}
