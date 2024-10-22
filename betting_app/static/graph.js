document.addEventListener('DOMContentLoaded', function () {
    // Fetch bankroll data from Flask
    fetch(graphDataUrl)
        .then(response => response.json())
        .then(data => {
            const dates = data.map(entry => new Date(entry.date));  // X-axis: dates
            const bankrolls = data.map(entry => entry.new_bankroll);  // Y-axis: bankroll values
            const betNames = data.map(entry => entry.bet_name);  // Bet names for tooltips

            // Create the chart after data is loaded
            const ctx = document.getElementById('bankrollChart').getContext('2d');
            const bankrollChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: dates,  // X-axis: dates
                    datasets: [{
                        label: 'Bankroll Over Time',
                        data: bankrolls,  // Y-axis: bankroll values
                        borderColor: 'rgba(75, 192, 192, 1)',  // Line color
                        backgroundColor: 'rgba(75, 192, 192, 0.1)',  // Background fill (if needed)
                        pointRadius: 5,
                        pointHoverRadius: 7,
                        fill: false,  // No background fill for a simple line
                    }]
                },
                options: {
                    scales: {
                        x: {
                            type: 'time',
                            time: {
                                unit: 'day',  // Display time by day
                                tooltipFormat: 'MMM dd, yyyy',  // Tooltip date format
                            },
                            ticks: {
                                autoSkip: true,
                                maxTicksLimit: 10,  // Limit the number of date labels on X-axis
                            },
                            title: {
                                display: true,
                                text: 'Date',  // Label for X-axis
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Bankroll ($)',  // Label for Y-axis
                            },
                        }
                    },
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const betName = betNames[context.dataIndex];
                                    const bankroll = context.raw;
                                    return `Bet: ${betName}, Bankroll: $${bankroll}`;
                                }
                            }
                        },
                    },
                    responsive: true
                }
            });
        })
        .catch(error => console.error('Error loading bankroll data:', error));
});