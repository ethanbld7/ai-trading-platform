
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
        