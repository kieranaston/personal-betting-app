document.addEventListener('DOMContentLoaded', function () {
    renderGraph();
});

function renderGraph() {
    fetch(graphDataUrl)
        .then(response => response.json())
        .then(responseData => {
            const dates = responseData.map(entry => new Date(entry.date));
            const bankrolls = responseData.map(entry => entry.new_bankroll);
            const chartData = {
                labels: dates,
                datasets: [{
                    label: 'Bankroll',
                    data: bankrolls,
                    borderColor: '#ffffff',
                    pointBackgroundColor: '#000000',
                    pointBorderColor: '#ffffff',
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    fill: false,
                    tension: 0.1
                }]
            };
            const config = {
                type: 'line',
                data: chartData,
                options: {
                    responsive: true,
                    scales: {
                        x: {
                            type: 'time',
                            time: {
                                unit: 'minute',
                                tooltipFormat: 'MMM dd, yyyy HH:mm',
                                displayFormats: {
                                    minute: 'MMM dd, HH:mm',
                                    hour: 'MMM dd, HH:mm',
                                }
                            },
                            title: {
                                display: true,
                                text: 'Date and Time'
                            },
                            ticks: {
                                autoSkip: true,
                                maxTicksLimit: 10,
                                maxRotation: 0,
                                minRotation: 0,
                                align: 'center',
                            },
                            grid: {
                                display: true,
                                color: 'rgba(255, 255, 255, 0.2)'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Bankroll ($)'
                            },
                            grid: {
                                display: true,
                                color: 'rgba(255, 255, 255, 0.2)'
                            }
                        }
                    },
                    plugins: {
                        tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            titleColor: '#ffffff',
                            bodyColor: '#ffffff'
                        }
                    }
                }
            };
            const ctx = document.getElementById('bankrollChart').getContext('2d');
            new Chart(ctx, config);
        })
        .catch(error => console.error('Error loading chart data:', error));
}