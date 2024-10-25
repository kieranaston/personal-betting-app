document.getElementById('ev-calc-form').addEventListener('submit', function(event) {
    event.preventDefault();
    calculateEV();
});

document.getElementById('place-bet-form').addEventListener('submit', function(event) {
    event.preventDefault();
    placeBet();
});

document.addEventListener('DOMContentLoaded', function () {
    fetch(latestBankrollUrl, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        const bankrollField = document.getElementById('enter-bankroll');
        bankrollField.value = data.latest_bankroll.toFixed(2);
    })
    .catch(error => {
        console.error('Error fetching latest bankroll:', error);
    });
});

function calculateEV() {
    const bankroll = document.getElementById('enter-bankroll').value;
    const unit_size = document.getElementById('enter-unit-size').value;
    const your_odds = document.getElementById('enter-your-odds').value;
    const other_odds = document.getElementById('enter-other-odds').value;
    const juice = document.getElementById('juice').value;

    const messageContainer = document.getElementById('ev-message-container');

    fetch(calculateEvUrl, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            bankroll: bankroll,
            unit_size: unit_size,
            your_odds: your_odds,
            other_odds: other_odds,
            juice: juice
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.ev && data.juice && data.kelly_units) {
            const evPercentage = (data.ev * 100).toFixed(2) + '%';
            const juicePercentage = (data.juice * 100).toFixed(2) + '%';
            let kellyUnitsHTML = '<ul>';
            Object.entries(data.kelly_units).forEach(([key, value]) => {
                kellyUnitsHTML += `<li>${key}: ${value.toFixed(2)}</li>`;
            });
            kellyUnitsHTML += '</ul>';
            document.getElementById('ev-result').innerHTML = `
                <p>EV: ${evPercentage}</p>
                <p>Juice: ${juicePercentage}</p>
                <p>Kelly Units:</p>
                ${kellyUnitsHTML}
            `;

            messageContainer.textContent = 'EV calculated successfully!';
            messageContainer.style.color = 'green';
        } else {
            messageContainer.textContent = 'Error calculating EV. Please check the input values.';
            messageContainer.style.color = 'red';
        }
    })
    .catch(error => {
        messageContainer.textContent = 'An error occurred while calculating EV.';
        messageContainer.style.color = 'red';
        console.error('Error:', error);
    });
}

function placeBet() {
    const bet_name = document.getElementById('bet-name').value;
    const kelly_percentage = document.getElementById('kelly-percentage').value;
    const bankroll = document.getElementById('enter-bankroll').value;
    const unit_size = document.getElementById('enter-unit-size').value;
    const your_odds = document.getElementById('enter-your-odds').value;
    const other_odds = document.getElementById('enter-other-odds').value;
    const manual_units_placed = document.getElementById('units-placed').value;

    const units_placed = manual_units_placed;

    const messageContainer = document.getElementById('bet-message-container');

    fetch(placeBetUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            bet_name: bet_name,
            units_placed: units_placed,
            bankroll: bankroll,
            unit_size: unit_size,
            your_odds: your_odds,
            other_odds: other_odds,
            kelly_percentage: kelly_percentage
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            messageContainer.textContent = `Error placing bet: ${data.error}`;
            messageContainer.style.color = 'red';
        } else {
            const bet_id = data.bet_id;
            messageContainer.textContent = 'Bet placed successfully!';
            messageContainer.style.color = 'green';
            getBetById(bet_id);
        }
    })
    .catch(error => {
        messageContainer.textContent = 'An error occurred while placing the bet.';
        messageContainer.style.color = 'red'; 
        console.error('Error:', error);
    });
}

function getBet(betId) {
    const url = getBetUrl.replace('0', betId);

    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('Error fetching bet:', data.error);
        } else {
            displayBet(data);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function getBetById(betId) {
    const url = getBetUrl.replace('0', betId);

    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('Error fetching bet:', data.error);
        } else {
            displayBet(data);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function displayBet(bet) {
    const betDetailsDiv = document.getElementById('bet-details');

    betDetailsDiv.innerHTML = '';

    const betInfo = `
        <h3>Bet Details</h3>
        <p><strong>Bet Name:</strong> ${bet.bet_name}</p>
        <p><strong>Date:</strong> ${bet.date}</p>
        <p><strong>Bankroll:</strong> $${bet.bankroll}</p>
        <p><strong>Unit Size:</strong> $${bet.unit_size}</p>
        <p><strong>Your Odds:</strong> ${bet.your_odds}</p>
        <p><strong>Other Odds:</strong> ${bet.other_odds}</p>
        <p><strong>Expected Value (EV):</strong> ${(bet.ev * 100).toFixed(2)}%</p>
        <p><strong>Units Placed:</strong> ${bet.units_placed}</p>
        <p><strong>Default juice:</strong> ${(bet.juice * 100).toFixed(2)}%</p>
    `;

    betDetailsDiv.innerHTML = betInfo;
}