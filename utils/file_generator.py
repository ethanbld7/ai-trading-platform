# utils/file_generator.py
"""
Utility functions to generate template and static files
"""
import os

def create_template_files():
    """
    Generate HTML template files
    """
    # Create templates directory if it doesn't exist
    os.makedirs("templates", exist_ok=True)
    
    # Main dashboard template
    with open("templates/index.html", "w") as f:
        f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI-Powered Hedge Fund Analytics</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.1/font/bootstrap-icons.css">
    <link rel="stylesheet" href="/static/css/styles.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/moment@2.29.4/moment.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-moment@1.0.1/dist/chartjs-adapter-moment.min.js"></script>
</head>
<body>
    <div class="container-fluid">
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container-fluid">
                <a class="navbar-brand" href="/">
                    <i class="bi bi-graph-up-arrow"></i> AI-Powered Hedge Fund Analytics
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav">
                        <li class="nav-item">
                            <a class="nav-link active" href="/">Dashboard</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/portfolio">Portfolio Simulator</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/predictions">Prediction History</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/api-docs">API</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>

        <div class="row mt-4">
            <div class="col-md-8">
                <div class="card shadow-sm mb-4">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">Price Chart</h5>
                        <div class="d-flex">
                            <select id="symbolSelector" class="form-select form-select-sm me-2">
                                {% for symbol in symbols %}
                                <option value="{{ symbol }}">{{ symbol }}</option>
                                {% endfor %}
                            </select>
                            <select id="timeframeSelector" class="form-select form-select-sm">
                                <option value="1m">1 Month</option>
                                <option value="3m" selected>3 Months</option>
                                <option value="6m">6 Months</option>
                                <option value="1y">1 Year</option>
                            </select>
                        </div>
                    </div>
                    <div class="card-body">
                        <canvas id="priceChart" height="300"></canvas>
                    </div>
                </div>

                <div class="row">
                    <div class="col-md-6">
                        <div class="card shadow-sm mb-4">
                            <div class="card-header">
                                <h5 class="mb-0">Feature Importance</h5>
                            </div>
                            <div class="card-body">
                                <canvas id="featureImportanceChart" height="250"></canvas>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card shadow-sm mb-4">
                            <div class="card-header">
                                <h5 class="mb-0">Volume Analysis</h5>
                            </div>
                            <div class="card-body">
                                <canvas id="volumeChart" height="250"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-md-4">
                <div class="card shadow-sm mb-4">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">AI Prediction</h5>
                    </div>
                    <div class="card-body" id="predictionCard">
                        <div class="text-center py-5">
                            <div class="spinner-border text-primary" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                            <p class="mt-3">Analyzing market data...</p>
                        </div>
                    </div>
                </div>

                <div class="card shadow-sm mb-4">
                    <div class="card-header">
                        <h5 class="mb-0">Key Statistics</h5>
                    </div>
                    <div class="card-body p-0">
                        <table class="table table-striped mb-0" id="statsTable">
                            <tbody>
                                <tr>
                                    <th>Open</th>
                                    <td id="statOpen">-</td>
                                </tr>
                                <tr>
                                    <th>Close</th>
                                    <td id="statClose">-</td>
                                </tr>
                                <tr>
                                    <th>Daily Range</th>
                                    <td id="statRange">-</td>
                                </tr>
                                <tr>
                                    <th>Volume</th>
                                    <td id="statVolume">-</td>
                                </tr>
                                <tr>
                                    <th>50-Day MA</th>
                                    <td id="statMA50">-</td>
                                </tr>
                                <tr>
                                    <th>Volatility</th>
                                    <td id="statVolatility">-</td>
                                </tr>
                                <tr>
                                    <th>Model Accuracy</th>
                                    <td id="statAccuracy">-</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div class="card shadow-sm mb-4">
                    <div class="card-header">
                        <h5 class="mb-0">Recent Predictions</h5>
                    </div>
                    <div class="card-body p-0">
                        <div class="list-group list-group-flush" id="recentPredictions">
                            <div class="text-center py-3">
                                <p class="text-muted">Loading predictions...</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <footer class="mt-5 mb-3 text-center text-muted">
            <p>AI-Powered Hedge Fund Analytics Dashboard &copy; 2025</p>
        </footer>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    <script src="/static/js/dashboard.js"></script>
</body>
</html>
        """)
    
    # Portfolio simulator template
    with open("templates/portfolio.html", "w") as f:
        f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portfolio Simulator - AI-Powered Hedge Fund Analytics</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.1/font/bootstrap-icons.css">
    <link rel="stylesheet" href="/static/css/styles.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/moment@2.29.4/moment.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-moment@1.0.1/dist/chartjs-adapter-moment.min.js"></script>
</head>
<body>
    <div class="container-fluid">
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container-fluid">
                <a class="navbar-brand" href="/">
                    <i class="bi bi-graph-up-arrow"></i> AI-Powered Hedge Fund Analytics
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav">
                        <li class="nav-item">
                            <a class="nav-link" href="/">Dashboard</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link active" href="/portfolio">Portfolio Simulator</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/predictions">Prediction History</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/api-docs">API</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>

        <div class="row mt-4">
            <div class="col-md-4">
                <div class="card shadow-sm mb-4">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">Simulation Settings</h5>
                    </div>
                    <div class="card-body">
                        <form id="simulationForm">
                            <div class="mb-3">
                                <label for="symbol" class="form-label">Stock Symbol</label>
                                <select id="symbol" name="symbol" class="form-select">
                                    {% for symbol in symbols %}
                                    <option value="{{ symbol }}">{{ symbol }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                            <div class="mb-3">
                                <label for="initialBalance" class="form-label">Initial Balance ($)</label>
                                <input type="number" class="form-control" id="initialBalance" name="initialBalance" value="10000" min="1000" max="1000000">
                            </div>
                            <div class="mb-3">
                                <label for="days" class="form-label">Simulation Period (Days)</label>
                                <select id="days" name="days" class="form-select">
                                    <option value="30">30 Days</option>
                                    <option value="60">60 Days</option>
                                    <option value="90" selected>90 Days</option>
                                    <option value="180">180 Days</option>
                                    <option value="365">365 Days</option>
                                </select>
                            </div>
                            <button type="submit" class="btn btn-primary w-100">Run Simulation</button>
                        </form>
                    </div>
                </div>
                
                <div class="card shadow-sm mb-4">
                    <div class="card-header">
                        <h5 class="mb-0">Simulation Results</h5>
                    </div>
                    <div class="card-body" id="resultsContainer">
                        <div class="text-center py-4">
                            <p class="text-muted">Run a simulation to see results</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-md-8">
                <div class="card shadow-sm mb-4">
                    <div class="card-header">
                        <h5 class="mb-0">Portfolio Performance</h5>
                    </div>
                    <div class="card-body">
                        <canvas id="portfolioChart" height="300"></canvas>
                    </div>
                </div>
                
                <div class="card shadow-sm mb-4">
                    <div class="card-header">
                        <h5 class="mb-0">Trading History</h5>
                    </div>
                    <div class="card-body p-0">
                        <div class="table-responsive">
                            <table class="table table-striped table-hover mb-0" id="tradesTable">
                                <thead>
                                    <tr>
                                        <th>Date</th>
                                        <th>Action</th>
                                        <th>Price</th>
                                        <th>Shares</th>
                                        <th>Value</th>
                                        <th>Confidence</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td colspan="6" class="text-center">No trades to display</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <footer class="mt-5 mb-3 text-center text-muted">
            <p>AI-Powered Hedge Fund Analytics Dashboard &copy; 2025</p>
        </footer>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    <script src="/static/js/portfolio.js"></script>
</body>
</html>
        """)
    
    # Predictions History template
    with open("templates/predictions.html", "w") as f:
        f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prediction History - AI-Powered Hedge Fund Analytics</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.1/font/bootstrap-icons.css">
    <link rel="stylesheet" href="/static/css/styles.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div class="container-fluid">
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container-fluid">
                <a class="navbar-brand" href="/">
                    <i class="bi bi-graph-up-arrow"></i> AI-Powered Hedge Fund Analytics
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav">
                        <li class="nav-item">
                            <a class="nav-link" href="/">Dashboard</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/portfolio">Portfolio Simulator</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link active" href="/predictions">Prediction History</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/api-docs">API</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>

        <div class="row mt-4">
            <div class="col-md-12">
                <div class="card shadow-sm mb-4">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">Prediction Accuracy</h5>
                        <div class="d-flex">
                            <select id="symbolSelector" class="form-select form-select-sm me-2">
                                {% for symbol in symbols %}
                                <option value="{{ symbol }}">{{ symbol }}</option>
                                {% endfor %}
                            </select>
                        </div>
                    </div>
                    <div class="card-body">
                        <canvas id="accuracyChart" height="200"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-md-12">
                <div class="card shadow-sm mb-4">
                    <div class="card-header">
                        <h5 class="mb-0">Prediction History</h5>
                    </div>
                    <div class="card-body p-0">
                        <div class="table-responsive">
                            <table class="table table-striped table-hover mb-0" id="predictionsTable">
                                <thead>
                                    <tr>
                                        <th>Date</th>
                                        <th>Symbol</th>
                                        <th>Predicted Movement</th>
                                        <th>Confidence</th>
                                        <th>Actual Movement</th>
                                        <th>Result</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td colspan="6" class="text-center">Loading prediction history...</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <footer class="mt-5 mb-3 text-center text-muted">
            <p>AI-Powered Hedge Fund Analytics Dashboard &copy; 2025</p>
        </footer>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    <script src="/static/js/predictions.js"></script>
</body>
</html>
        """)
        
    # API Documentation template
    with open("templates/api-docs.html", "w") as f:
        f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Documentation - AI-Powered Hedge Fund Analytics</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.1/font/bootstrap-icons.css">
    <link rel="stylesheet" href="/static/css/styles.css">
</head>
<body>
    <div class="container-fluid">
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container-fluid">
                <a class="navbar-brand" href="/">
                    <i class="bi bi-graph-up-arrow"></i> AI-Powered Hedge Fund Analytics
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav">
                        <li class="nav-item">
                            <a class="nav-link" href="/">Dashboard</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/portfolio">Portfolio Simulator</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/predictions">Prediction History</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link active" href="/api-docs">API</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>

        <div class="row mt-4">
            <div class="col-md-12">
                <div class="card shadow-sm mb-4">
                    <div class="card-header">
                        <h5 class="mb-0">API Documentation</h5>
                    </div>
                    <div class="card-body">
                        <h2>Overview</h2>
                        <p>
                            The AI-Powered Hedge Fund Analytics API provides programmatic access to stock data, predictions, and portfolio simulations.
                            All endpoints return JSON data and accept various parameters to customize the response.
                        </p>
                        
                        <hr>
                        
                        <h3>Endpoints</h3>
                        
                        <div class="card mb-4">
                            <div class="card-header">
                                <h5 class="mb-0">GET /api/stock/{symbol}</h5>
                            </div>
                            <div class="card-body">
                                <p>Retrieve historical stock data for a specific symbol.</p>
                                
                                <h6>Parameters:</h6>
                                <ul>
                                    <li><code>symbol</code> (path) - Stock symbol (e.g., AAPL)</li>
                                    <li><code>period</code> (query, optional) - Time period (default: "3m", options: "1m", "3m", "6m", "1y")</li>
                                </ul>
                                
                                <h6>Example:</h6>
                                <pre><code>GET /api/stock/AAPL?period=3m</code></pre>
                            </div>
                        </div>
                        
                        <div class="card mb-4">
                            <div class="card-header">
                                <h5 class="mb-0">GET /api/predict/{symbol}</h5>
                            </div>
                            <div class="card-body">
                                <p>Get AI prediction for a stock's next-day movement.</p>
                                
                                <h6>Parameters:</h6>
                                <ul>
                                    <li><code>symbol</code> (path) - Stock symbol (e.g., AAPL)</li>
                                </ul>
                                
                                <h6>Example:</h6>
                                <pre><code>GET /api/predict/MSFT</code></pre>
                            </div>
                        </div>
                        
                        <div class="card mb-4">
                            <div class="card-header">
                                <h5 class="mb-0">GET /api/portfolio/simulate</h5>
                            </div>
                            <div class="card-body">
                                <p>Run a portfolio simulation based on AI predictions.</p>
                                
                                <h6>Parameters:</h6>
                                <ul>
                                    <li><code>symbol</code> (query) - Stock symbol (e.g., AAPL)</li>
                                    <li><code>days</code> (query, optional) - Simulation period in days (default: 90)</li>
                                    <li><code>initial_balance</code> (query, optional) - Starting portfolio balance (default: 10000)</li>
                                </ul>
                                
                                <h6>Example:</h6>
                                <pre><code>GET /api/portfolio/simulate?symbol=TSLA&days=60&initial_balance=15000</code></pre>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <footer class="mt-5 mb-3 text-center text-muted">
            <p>AI-Powered Hedge Fund Analytics Dashboard &copy; 2025</p>
        </footer>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
        """)

def create_static_files():
    """
    Generate CSS and JavaScript files
    """
    # Create static directories if they don't exist
    os.makedirs("static/css", exist_ok=True)
    os.makedirs("static/js", exist_ok=True)
    
    # CSS Styles
    with open("static/css/styles.css", "w") as f:
        f.write("""
body {
    background-color: #f8f9fa;
}

.navbar-brand {
    font-weight: 600;
}

.card {
    border: none;
    border-radius: 10px;
}

.card-header {
    border-radius: 10px 10px 0 0 !important;
    font-weight: 500;
}

.prediction-up {
    color: #198754;
}

.prediction-down {
    color: #dc3545;
}

.confidence-meter {
    height: 8px;
    border-radius: 4px;
    margin-top: 5px;
}

.confidence-low {
    background-color: #ffc107;
}

.confidence-medium {
    background-color: #0dcaf0;
}

.confidence-high {
    background-color: #198754;
}

.list-group-item {
    border-left: none;
    border-right: none;
}

.prediction-item {
    border-left: 4px solid;
}

.prediction-item.correct {
    border-left-color: #198754;
}

.prediction-item.incorrect {
    border-left-color: #dc3545;
}

.prediction-item.pending {
    border-left-color: #0dcaf0;
}

.badge {
    font-weight: 500;
}
        """)
    
    # Create JavaScript files
    create_dashboard_js()
    create_portfolio_js()
    create_predictions_js()


def create_portfolio_js():
    """Create the portfolio.js file"""
    with open("static/js/portfolio.js", "w") as f:
        f.write("""
// Initialize charts
let portfolioChart;

// DOM elements
const simulationForm = document.getElementById('simulationForm');
const resultsContainer = document.getElementById('resultsContainer');
const tradesTable = document.getElementById('tradesTable');

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    simulationForm.addEventListener('submit', function(e) {
        e.preventDefault();
        runSimulation();
    });
});

// Run portfolio simulation
function runSimulation() {
    // Show loading
    resultsContainer.innerHTML = `
        <div class="text-center py-4">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-3">Running simulation...</p>
        </div>
    `;
    
    // Get form values
    const symbol = document.getElementById('symbol').value;
    const initialBalance = document.getElementById('initialBalance').value;
    const days = document.getElementById('days').value;
    
    // Call API
    fetch(`/api/portfolio/simulate?symbol=${symbol}&initial_balance=${initialBalance}&days=${days}`)
        .then(response => response.json())
        .then(data => {
            updateResults(data);
            updatePortfolioChart(data);
            updateTradesTable(data);
        })
        .catch(error => {
            resultsContainer.innerHTML = `
                <div class="alert alert-danger">
                    Error running simulation: ${error.message}
                </div>
            `;
        });
}

// Update simulation results
function updateResults(data) {
    if (!data) {
        resultsContainer.innerHTML = `
            <div class="alert alert-warning">
                Could not run simulation with the selected parameters.
            </div>
        `;
        return;
    }
    
    const roi = data.roi_percentage.toFixed(2);
    const roiClass = roi >= 0 ? 'text-success' : 'text-danger';
    
    const buyHoldRoi = data.buy_and_hold.roi_percentage.toFixed(2);
    const buyHoldRoiClass = buyHoldRoi >= 0 ? 'text-success' : 'text-danger';
    
    const strategy = roi > buyHoldRoi ? 'AI-driven' : 'Buy & Hold';
    
    resultsContainer.innerHTML = `
        <div class="mb-3">
            <div class="row">
                <div class="col">
                    <h6 class="text-muted">Initial Balance</h6>
                    <h4>$${data.initial_balance.toLocaleString()}</h4>
                </div>
                <div class="col">
                    <h6 class="text-muted">Final Balance</h6>
                    <h4>$${data.final_balance.toLocaleString()}</h4>
                </div>
            </div>
        </div>
        
        <div class="mb-3">
            <h6 class="text-muted">Return on Investment</h6>
            <h3 class="${roiClass}">${roi}%</h3>
        </div>
        
        <div class="mb-3">
            <h6 class="text-muted">Buy & Hold ROI</h6>
            <h5 class="${buyHoldRoiClass}">${buyHoldRoi}%</h5>
        </div>
        
        <div class="mb-3">
            <h6 class="text-muted">Best Strategy</h6>
            <h5>${strategy}</h5>
        </div>
        
        <div class="mb-3">
            <h6 class="text-muted">Total Trades</h6>
            <h5>${data.trades.length}</h5>
        </div>
    `;
}

// Update portfolio chart
function updatePortfolioChart(data) {
    if (!data || !data.daily_balance) return;
    
    const ctx = document.getElementById('portfolioChart').getContext('2d');
    
    // Prepare data
    const dates = data.daily_balance.map(day => day.date);
    const aiBalance = data.daily_balance.map(day => day.balance);
    
    // Calculate buy & hold balance for each day
    const initialShares = data.initial_balance / data.daily_balance[0].price;
    const buyHoldBalance = data.daily_balance.map(day => initialShares * day.price);
    
    // Destroy existing chart if it exists
    if (portfolioChart) {
        portfolioChart.destroy();
    }
    
    // Create new chart
    portfolioChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [
                {
                    label: 'AI Strategy',
                    data: aiBalance,
                    borderColor: '#0d6efd',
                    backgroundColor: 'rgba(13, 110, 253, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.1
                },
                {
                    label: 'Buy & Hold',
                    data: buyHoldBalance,
                    borderColor: '#6c757d',
                    backgroundColor: 'rgba(108, 117, 125, 0.1)',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    fill: true,
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += '$' + context.parsed.y.toFixed(2);
                            }
                            return label;
                        }
                    }
                }
            },
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day'
                    },
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Portfolio Value ($)'
                    }
                }
            }
        }
    });
}

// Update trades table
function updateTradesTable(data) {
    if (!data || !data.trades || !data.trades.length) {
        tradesTable.querySelector('tbody').innerHTML = `
            <tr>
                <td colspan="6" class="text-center">No trades to display</td>
            </tr>
        `;
        return;
    }
    
    let html = '';
    
    data.trades.forEach(trade => {
        const actionClass = trade.action === 'BUY' ? 'text-primary' : 
                          (trade.action === 'SELL' ? 'text-danger' : 'text-success');
        
        html += `
            <tr>
                <td>${trade.date}</td>
                <td class="${actionClass} fw-bold">${trade.action}</td>
                <td>$${trade.price.toFixed(2)}</td>
                <td>${trade.shares.toFixed(2)}</td>
                <td>$${trade.value.toFixed(2)}</td>
                <td>${(trade.confidence * 100).toFixed(0)}%</td>
            </tr>
        `;
    });
    
    tradesTable.querySelector('tbody').innerHTML = html;
}
        """)

def create_predictions_js():
    """Create the predictions.js file"""
    with open("static/js/predictions.js", "w") as f:
        f.write("""
// Initialize charts
let accuracyChart;

// DOM elements
const symbolSelector = document.getElementById('symbolSelector');
const predictionsTable = document.getElementById('predictionsTable');

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    loadData();
    
    symbolSelector.addEventListener('change', function() {
        loadData();
    });
});

// Load prediction data
function loadData() {
    const symbol = symbolSelector.value;
    
    // Load prediction history
    fetch(`/api/predictions/history?symbol=${symbol}`)
        .then(response => response.json())
        .then(data => {
            updatePredictionsTable(data);
            updateAccuracyChart(data);
        });
}

// Update predictions table
function updatePredictionsTable(data) {
    if (!data || !data.length) {
        predictionsTable.querySelector('tbody').innerHTML = `
            <tr>
                <td colspan="6" class="text-center">No prediction history available</td>
            </tr>
        `;
        return;
    }
    
    let html = '';
    
    data.forEach(pred => {
        let resultHtml = '';
        
        if (pred.actual_movement !== null) {
            const isCorrect = pred.predicted_movement === pred.actual_movement;
            resultHtml = isCorrect ? 
                `<span class="badge bg-success">Correct</span>` : 
                `<span class="badge bg-danger">Incorrect</span>`;
        } else {
            resultHtml = `<span class="badge bg-info">Pending</span>`;
        }
        
        html += `
            <tr>
                <td>${pred.date}</td>
                <td>${pred.symbol}</td>
                <td class="prediction-${pred.predicted_movement ? 'up' : 'down'}">
                    <i class="bi bi-arrow-${pred.predicted_movement ? 'up' : 'down'}-circle-fill"></i>
                    ${pred.predicted_movement ? 'Up' : 'Down'}
                </td>
                <td>${(pred.confidence * 100).toFixed(0)}%</td>
                <td>
                    ${pred.actual_movement !== null ? 
                        `<i class="bi bi-arrow-${pred.actual_movement ? 'up' : 'down'}-circle-fill"></i>
                         ${pred.actual_movement ? 'Up' : 'Down'}` : 
                        'Pending'}
                </td>
                <td>${resultHtml}</td>
            </tr>
        `;
    });
    
    predictionsTable.querySelector('tbody').innerHTML = html;
}

// Update accuracy chart
function updateAccuracyChart(data) {
    if (!data || !data.length) return;
    
    const ctx = document.getElementById('accuracyChart').getContext('2d');
    
    // Filter completed predictions
    const completedPredictions = data.filter(pred => pred.actual_movement !== null);
    
    if (!completedPredictions.length) return;
    
    // Group by week
    const groupedByWeek = {};
    
    completedPredictions.forEach(pred => {
        const date = new Date(pred.date);
        const weekStart = new Date(date);
        weekStart.setDate(date.getDate() - date.getDay());
        const weekKey = weekStart.toISOString().slice(0, 10);
        
        if (!groupedByWeek[weekKey]) {
            groupedByWeek[weekKey] = {
                total: 0,
                correct: 0
            };
        }
        
        groupedByWeek[weekKey].total++;
        if (pred.predicted_movement === pred.actual_movement) {
            groupedByWeek[weekKey].correct++;
        }
    });
    
    // Convert to array and sort by date
    const weeklyData = Object.keys(groupedByWeek)
        .map(week => {
            return {
                week,
                accuracy: (groupedByWeek[week].correct / groupedByWeek[week].total) * 100
            };
        })
        .sort((a, b) => a.week.localeCompare(b.week));
    
    // Destroy existing chart if it exists
    if (accuracyChart) {
        accuracyChart.destroy();
    }
    
    // Create new chart
    accuracyChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: weeklyData.map(item => item.week),
            datasets: [{
                label: 'Weekly Accuracy (%)',
                data: weeklyData.map(item => item.accuracy),
                borderColor: '#0d6efd',
                backgroundColor: 'rgba(13, 110, 253, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Accuracy: ${context.parsed.y.toFixed(1)}%`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    min: 0,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Accuracy (%)'
                    }
                }
            }
        }
    });
}
        """)

def create_portfolio_js():
    """Create the portfolio.js file"""
    with open("static/js/portfolio.js", "w") as f:
        f.write("""
// Initialize charts
let portfolioChart;

// DOM elements
const simulationForm = document.getElementById('simulationForm');
const resultsContainer = document.getElementById('resultsContainer');
const tradesTable = document.getElementById('tradesTable');

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    simulationForm.addEventListener('submit', function(e) {
        e.preventDefault();
        runSimulation();
    });
});

// Run portfolio simulation
function runSimulation() {
    // Show loading
    resultsContainer.innerHTML = `
        <div class="text-center py-4">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-3">Running simulation...</p>
        </div>
    `;
    
    // Get form values
    const symbol = document.getElementById('symbol').value;
    const initialBalance = document.getElementById('initialBalance').value;
    const days = document.getElementById('days').value;
    
    // Call API
    fetch(`/api/portfolio/simulate?symbol=${symbol}&initial_balance=${initialBalance}&days=${days}`)
        .then(response => response.json())
        .then(data => {
            updateResults(data);
            updatePortfolioChart(data);
            updateTradesTable(data);
        })
        .catch(error => {
            resultsContainer.innerHTML = `
                <div class="alert alert-danger">
                    Error running simulation: ${error.message}
                </div>
            `;
        });
}

// Update simulation results
function updateResults(data) {
    if (!data) {
        resultsContainer.innerHTML = `
            <div class="alert alert-warning">
                Could not run simulation with the selected parameters.
            </div>
        `;
        return;
    }
    
    const roi = data.roi_percentage.toFixed(2);
    const roiClass = roi >= 0 ? 'text-success' : 'text-danger';
    
    const buyHoldRoi = data.buy_and_hold.roi_percentage.toFixed(2);
    const buyHoldRoiClass = buyHoldRoi >= 0 ? 'text-success' : 'text-danger';
    
    const strategy = roi > buyHoldRoi ? 'AI-driven' : 'Buy & Hold';
    
    resultsContainer.innerHTML = `
        <div class="mb-3">
            <div class="row">
                <div class="col">
                    <h6 class="text-muted">Initial Balance</h6>
                    <h4>$${data.initial_balance.toLocaleString()}</h4>
                </div>
                <div class="col">
                    <h6 class="text-muted">Final Balance</h6>
                    <h4>$${data.final_balance.toLocaleString()}</h4>
                </div>
            </div>
        </div>
        
        <div class="mb-3">
            <h6 class="text-muted">Return on Investment</h6>
            <h3 class="${roiClass}">${roi}%</h3>
        </div>
        
        <div class="mb-3">
            <h6 class="text-muted">Buy & Hold ROI</h6>
            <h5 class="${buyHoldRoiClass}">${buyHoldRoi}%</h5>
        </div>
        
        <div class="mb-3">
            <h6 class="text-muted">Best Strategy</h6>
            <h5>${strategy}</h5>
        </div>
        
        <div class="mb-3">
            <h6 class="text-muted">Total Trades</h6>
            <h5>${data.trades.length}</h5>
        </div>
    `;
}

// Update portfolio chart
function updatePortfolioChart(data) {
    if (!data || !data.daily_balance) return;
    
    const ctx = document.getElementById('portfolioChart').getContext('2d');
    
    // Prepare data
    const dates = data.daily_balance.map(day => day.date);
    const aiBalance = data.daily_balance.map(day => day.balance);
    
    // Calculate buy & hold balance for each day
    const initialShares = data.initial_balance / data.daily_balance[0].price;
    const buyHoldBalance = data.daily_balance.map(day => initialShares * day.price);
    
    // Destroy existing chart if it exists
    if (portfolioChart) {
        portfolioChart.destroy();
    }
    
    // Create new chart
    portfolioChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [
                {
                    label: 'AI Strategy',
                    data: aiBalance,
                    borderColor: '#0d6efd',
                    backgroundColor: 'rgba(13, 110, 253, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.1
                },
                {
                    label: 'Buy & Hold',
                    data: buyHoldBalance,
                    borderColor: '#6c757d',
                    backgroundColor: 'rgba(108, 117, 125, 0.1)',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    fill: true,
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += '$' + context.parsed.y.toFixed(2);
                            }
                            return label;
                        }
                    }
                }
            },
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day'
                    },
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Portfolio Value ($)'
                    }
                }
            }
        }
    });
}

// Update trades table
function updateTradesTable(data) {
    if (!data || !data.trades || !data.trades.length) {
        tradesTable.querySelector('tbody').innerHTML = `
            <tr>
                <td colspan="6" class="text-center">No trades to display</td>
            </tr>
        `;
        return;
    }
    
    let html = '';
    
    data.trades.forEach(trade => {
        const actionClass = trade.action === 'BUY' ? 'text-primary' : 
                          (trade.action === 'SELL' ? 'text-danger' : 'text-success');
        
        html += `
            <tr>
                <td>${trade.date}</td>
                <td class="${actionClass} fw-bold">${trade.action}</td>
                <td>$${trade.price.toFixed(2)}</td>
                <td>${trade.shares.toFixed(2)}</td>
                <td>$${trade.value.toFixed(2)}</td>
                <td>${(trade.confidence * 100).toFixed(0)}%</td>
            </tr>
        `;
    });
    
    tradesTable.querySelector('tbody').innerHTML = html;
}
        """)

def create_predictions_js():
    """Create the predictions.js file"""
    with open("static/js/predictions.js", "w") as f:
        f.write("""
// Initialize charts
let accuracyChart;

// DOM elements
const symbolSelector = document.getElementById('symbolSelector');
const predictionsTable = document.getElementById('predictionsTable');

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    loadData();
    
    symbolSelector.addEventListener('change', function() {
        loadData();
    });
});

// Load prediction data
function loadData() {
    const symbol = symbolSelector.value;
    
    // Load prediction history
    fetch(`/api/predictions/history?symbol=${symbol}`)
        .then(response => response.json())
        .then(data => {
            updatePredictionsTable(data);
            updateAccuracyChart(data);
        });
}

// Update predictions table
function updatePredictionsTable(data) {
    if (!data || !data.length) {
        predictionsTable.querySelector('tbody').innerHTML = `
            <tr>
                <td colspan="6" class="text-center">No prediction history available</td>
            </tr>
        `;
        return;
    }
    
    let html = '';
    
    data.forEach(pred => {
        let resultHtml = '';
        
        if (pred.actual_movement !== null) {
            const isCorrect = pred.predicted_movement === pred.actual_movement;
            resultHtml = isCorrect ? 
                `<span class="badge bg-success">Correct</span>` : 
                `<span class="badge bg-danger">Incorrect</span>`;
        } else {
            resultHtml = `<span class="badge bg-info">Pending</span>`;
        }
        
        html += `
            <tr>
                <td>${pred.date}</td>
                <td>${pred.symbol}</td>
                <td class="prediction-${pred.predicted_movement ? 'up' : 'down'}">
                    <i class="bi bi-arrow-${pred.predicted_movement ? 'up' : 'down'}-circle-fill"></i>
                    ${pred.predicted_movement ? 'Up' : 'Down'}
                </td>
                <td>${(pred.confidence * 100).toFixed(0)}%</td>
                <td>
                    ${pred.actual_movement !== null ? 
                        `<i class="bi bi-arrow-${pred.actual_movement ? 'up' : 'down'}-circle-fill"></i>
                         ${pred.actual_movement ? 'Up' : 'Down'}` : 
                        'Pending'}
                </td>
                <td>${resultHtml}</td>
            </tr>
        `;
    });
    
    predictionsTable.querySelector('tbody').innerHTML = html;
}

// Update accuracy chart
function updateAccuracyChart(data) {
    if (!data || !data.length) return;
    
    const ctx = document.getElementById('accuracyChart').getContext('2d');
    
    // Filter completed predictions
    const completedPredictions = data.filter(pred => pred.actual_movement !== null);
    
    if (!completedPredictions.length) return;
    
    // Group by week
    const groupedByWeek = {};
    
    completedPredictions.forEach(pred => {
        const date = new Date(pred.date);
        const weekStart = new Date(date);
        weekStart.setDate(date.getDate() - date.getDay());
        const weekKey = weekStart.toISOString().slice(0, 10);
        
        if (!groupedByWeek[weekKey]) {
            groupedByWeek[weekKey] = {
                total: 0,
                correct: 0
            };
        }
        
        groupedByWeek[weekKey].total++;
        if (pred.predicted_movement === pred.actual_movement) {
            groupedByWeek[weekKey].correct++;
        }
    });
    
    // Convert to array and sort by date
    const weeklyData = Object.keys(groupedByWeek)
        .map(week => {
            return {
                week,
                accuracy: (groupedByWeek[week].correct / groupedByWeek[week].total) * 100
            };
        })
        .sort((a, b) => a.week.localeCompare(b.week));
    
    // Destroy existing chart if it exists
    if (accuracyChart) {
        accuracyChart.destroy();
    }
    
    // Create new chart
    accuracyChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: weeklyData.map(item => item.week),
            datasets: [{
                label: 'Weekly Accuracy (%)',
                data: weeklyData.map(item => item.accuracy),
                borderColor: '#0d6efd',
                backgroundColor: 'rgba(13, 110, 253, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Accuracy: ${context.parsed.y.toFixed(1)}%`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    min: 0,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Accuracy (%)'
                    }
                }
            }
        }
    });
}
        """)

def create_dashboard_js():
    """Create the dashboard.js file"""
    with open("static/js/dashboard.js", "w") as f:
        f.write("""
// Initialize charts
let priceChart, featureImportanceChart, volumeChart;
let currentSymbol = 'AAPL';
let currentTimeframe = '3m';

// DOM elements
const symbolSelector = document.getElementById('symbolSelector');
const timeframeSelector = document.getElementById('timeframeSelector');

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    loadData();
    
    symbolSelector.addEventListener('change', function() {
        currentSymbol = this.value;
        loadData();
    });
    
    timeframeSelector.addEventListener('change', function() {
        currentTimeframe = this.value;
        loadData();
    });
});

// Load all data for the dashboard
function loadData() {
    // Show loading state
    document.getElementById('predictionCard').innerHTML = `
        <div class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-3">Analyzing market data...</p>
        </div>
    `;
    
    // Load price data
    fetch(`/api/stock/${currentSymbol}?period=${currentTimeframe}`)
        .then(response => response.json())
        .then(data => {
            updatePriceChart(data);
            updateVolumeChart(data);
        });
    
    // Load prediction
    fetch(`/api/predict/${currentSymbol}`)
        .then(response => response.json())
        .then(data => {
            updatePredictionCard(data);
            updateStatsTable(data);
            updateFeatureImportanceChart(data);
        });
    
    // Load recent predictions
    fetch(`/api/predictions/recent?symbol=${currentSymbol}&limit=5`)
        .then(response => response.json())
        .then(data => {
            updateRecentPredictions(data);
        });
}

// Update the price chart
function updatePriceChart(data) {
    const ctx = document.getElementById('priceChart').getContext('2d');
    
    // Prepare data
    const dates = data.map(item => item.date);
    const prices = data.map(item => item.close_price);
    
    // Destroy existing chart if it exists
    if (priceChart) {
        priceChart.destroy();
    }
    
    // Create new chart
    priceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: `${currentSymbol} Price`,
                data: prices,
                borderColor: '#0d6efd',
                backgroundColor: 'rgba(13, 110, 253, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day'
                    },
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Price ($)'
                    }
                }
            }
        }
    });
}

// Update the volume chart
function updateVolumeChart(data) {
    const ctx = document.getElementById('volumeChart').getContext('2d');
    
    // Prepare data
    const dates = data.map(item => item.date);
    const volumes = data.map(item => item.volume);
    
    // Get only last 30 data points for cleaner chart
    const recentDates = dates.slice(-30);
    const recentVolumes = volumes.slice(-30);
    
    // Destroy existing chart if it exists
    if (volumeChart) {
        volumeChart.destroy();
    }
    
    // Create new chart
    volumeChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: recentDates,
            datasets: [{
                label: 'Volume',
                data: recentVolumes,
                backgroundColor: 'rgba(108, 117, 125, 0.7)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Volume'
                    }
                }
            }
        }
    });
}

// Update the feature importance chart
function updateFeatureImportanceChart(data) {
    if (!data.feature_importance) return;
    
    const ctx = document.getElementById('featureImportanceChart').getContext('2d');
    
    // Prepare data
    const features = data.feature_importance.features.map(f => {
        // Make feature names more readable
        return f.replace('_', ' ').replace('price', '').trim();
    });
    const importance = data.feature_importance.importance;
    
    // Sort by importance
    const combined = features.map((f, i) => {
        return { feature: f, importance: importance[i] };
    }).sort((a, b) => b.importance - a.importance);
    
    // Take top 6 features
    const topFeatures = combined.slice(0, 6);
    
    // Destroy existing chart if it exists
    if (featureImportanceChart) {
        featureImportanceChart.destroy();
    }
    
    // Create new chart
    featureImportanceChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: topFeatures.map(item => item.feature),
            datasets: [{
                label: 'Importance',
                data: topFeatures.map(item => item.importance),
                backgroundColor: [
                    '#0d6efd', '#6610f2', '#6f42c1', 
                    '#d63384', '#dc3545', '#fd7e14'
                ]
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Importance'
                    }
                }
            }
        }
    });
}

// Update the prediction card
function updatePredictionCard(data) {
    if (!data.prediction) return;
    
    const prediction = data.prediction.movement;
    const confidence = data.prediction.confidence;
    const confidencePercentage = Math.round(confidence * 100);
    
    let confidenceClass = 'confidence-low';
    if (confidence > 0.7) {
        confidenceClass = 'confidence-high';
    } else if (confidence > 0.55) {
        confidenceClass = 'confidence-medium';
    }
    
    document.getElementById('predictionCard').innerHTML = `
        <div class="text-center">
            <h3 class="prediction-${prediction ? 'up' : 'down'}">
                <i class="bi bi-arrow-${prediction ? 'up' : 'down'}-circle-fill"></i> 
                ${prediction ? 'Upward' : 'Downward'} Movement Predicted
            </h3>
            <p class="mb-1">Confidence: ${confidencePercentage}%</p>
            <div class="progress confidence-meter mb-3">
                <div class="${confidenceClass}" style="width: ${confidencePercentage}%"></div>
            </div>
            <p class="mb-0 small text-muted">Prediction for ${data.latest.formatted_date}</p>
        </div>
    `;
}

// Update stats table
function updateStatsTable(data) {
    if (!data.latest) return;
    
    const latest = data.latest;
    
    document.getElementById('statOpen').textContent = `$${latest.open_price.toFixed(2)}`;
    document.getElementById('statClose').textContent = `$${latest.close_price.toFixed(2)}`;
    document.getElementById('statRange').textContent = `$${latest.low_price.toFixed(2)} - $${latest.high_price.toFixed(2)}`;
    document.getElementById('statVolume').textContent = latest.volume.toLocaleString();
    
    if (latest.ma50) {
        document.getElementById('statMA50').textContent = `$${latest.ma50.toFixed(2)}`;
    }
    
    if (latest.volatility) {
        document.getElementById('statVolatility').textContent = `${(latest.volatility * 100).toFixed(2)}%`;
    }
    
    if (data.model_accuracy) {
        document.getElementById('statAccuracy').textContent = `${(data.model_accuracy * 100).toFixed(1)}%`;
    }
}

// Update recent predictions list
function updateRecentPredictions(data) {
    if (!data || !data.length) {
        document.getElementById('recentPredictions').innerHTML = `
            <div class="text-center py-3">
                <p class="text-muted">No recent predictions available</p>
            </div>
        `;
        return;
    }
    
    let html = '';
    
    data.forEach(pred => {
        let statusClass = 'pending';
        let statusBadge = `<span class="badge bg-info">Pending</span>`;
        
        if (pred.actual_movement !== null) {
            const isCorrect = pred.predicted_movement === pred.actual_movement;
            statusClass = isCorrect ? 'correct' : 'incorrect';
            statusBadge = isCorrect ? 
                `<span class="badge bg-success">Correct</span>` : 
                `<span class="badge bg-danger">Incorrect</span>`;
        }
        
        html += `
            <div class="list-group-item prediction-item ${statusClass}">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h6 class="mb-0">${pred.date}</h6>
                        <p class="mb-0 small text-muted">
                            Predicted: 
                            <span class="prediction-${pred.predicted_movement ? 'up' : 'down'}">
                                <i class="bi bi-arrow-${pred.predicted_movement ? 'up' : 'down'}-circle-fill"></i>
                                ${pred.predicted_movement ? 'Up' : 'Down'}
                            </span>
                        </p>
                    </div>
                    <div class="text-center">
                        ${statusBadge}
                        <div class="small text-muted">${Math.round(pred.confidence * 100)}% confidence</div>
                    </div>
                </div>
            </div>
        `;
    });
    
    document.getElementById('recentPredictions').innerHTML = html;
}
        """)