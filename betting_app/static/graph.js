document.addEventListener('DOMContentLoaded', function () {
    fetch(graphDataUrl)
        .then(response => response.json())
        .then(data => {
            const dates = data.map(entry => new Date(entry.date));
            const bankrolls = data.map(entry => entry.new_bankroll);
            const betNames = data.map(entry => entry.bet_name);

            const ctx = document.getElementById('bankrollChart').getContext('2d');
            const bankrollChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: dates,
                    datasets: [{
                        label: 'Bankroll Over Time',
                        data: bankrolls,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        backgroundColor: 'rgba(75, 192, 192, 0.1)',
                        pointRadius: 5,
                        pointHoverRadius: 7,
                        fill: false,
                    }]
                },
                options: {
                    scales: {
                        x: {
                            type: 'time',
                            time: {
                                unit: 'day',
                                tooltipFormat: 'MMM dd, yyyy',
                            },
                            ticks: {
                                autoSkip: true,
                                maxTicksLimit: 10,
                            },
                            title: {
                                display: true,
                                text: 'Date',
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Bankroll ($)', 
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