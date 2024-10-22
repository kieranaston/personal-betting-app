document.getElementById('backup-btn').addEventListener('click', function() {
    fetch(backupBetsUrl, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            console.log(data.message);
        } else if (data.error) {
            console.log('Error: ' + data.error);
        }
    })
    .catch(error => {
        console.log('An error occurred while backing up the database.');
        console.error(error);
    });
});

function updateBetStatus(url, newStatus) {
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'status': newStatus
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => { throw new Error(text); });
        }
        return response.json();
    })
    .then(data => {
        if (data.message) {
            console.log(data.message);
            updateProfitLoss(url.replace('update-bet-status', 'update-profit-loss'))
                .then(() => {
                    updateBankroll(url.replace('update-bet-status', 'update-bankroll'));
                });
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function updateProfitLoss(url) {
    return fetch(url, {
        method: 'POST'
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => { throw new Error(text); });
        }
        return response.json();
    })
    .then(data => {
        console.log(data.message);
        const betId = url.split('/').pop();
        document.getElementById(`profit-loss-${betId}`).textContent = parseFloat(data.profit_loss).toFixed(2);
    })
    .catch(error => {
        console.error('Error updating profit/loss:', error);
    });
}

function updateBankroll(url) {
    fetch(url, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
    })
    .catch(error => {
        console.error('Error updating bankroll:', error);
    });
}