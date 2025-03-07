
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
        