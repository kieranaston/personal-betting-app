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
                    borderColor: '#000000',
                    pointBackgroundColor: 'rgba(255, 255, 255, 0)',
                    pointBorderColor: '#000000',
                    pointRadius: 4.5,
                    pointHoverRadius: 6,
                    fill: true,
                    backgroundColor: 'rgba(169, 169, 169, 0.2)'
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
                                unit: 'day',
                                tooltipFormat: 'MMM dd, yyyy',
                                displayFormats: {
                                    day: 'MMM dd',
                                }
                            },
                            ticks: {
                                color: '#000000',
                                autoSkip: true,
                                maxTicksLimit: 10,
                                maxRotation: 0,
                                minRotation: 0,
                                align: 'center',
                            },
                            title: {
                                display: true,
                                text: 'Date',
                                color: '#000000'
                            },
                            grid: {
                                display: true,
                                color: '#d3d3d3'
                            }
                        },
                        y: {
                            ticks: {
                                color: '#000000',
                                stepSize: 10,
                            },
                            title: {
                                display: true,
                                text: 'Bankroll ($)',
                                color: '#000000'
                            },
                            grid: {
                                display: true,
                                color: '#d3d3d3'
                            }
                        }
                    },
                    plugins: {
                        tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            titleColor: '#ffffff',
                            bodyColor: '#ffffff'
                        },
                        legend: {
                            display: false  
                        }
                    }
                }
            };
            const ctx = document.getElementById('bankrollChart').getContext('2d');
            new Chart(ctx, config);
        })
        .catch(error => console.error('Error loading chart data:', error));
}