
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
        