import re

def implied_probability(odds):
    print(f"Calculating implied probability for odds: {odds}")
    if '/' in odds:
        side1, side2 = odds.split('/')
        side1 = int(side1.strip())
        side2 = int(side2.strip())

        prob1 = 100 / (side1 + 100) if side1 > 0 else abs(side1) / (abs(side1) + 100)
        prob2 = 100 / (side2 + 100) if side2 > 0 else abs(side2) / (abs(side2) + 100)

        print(f"Implied Probabilities for {odds}: {prob1:.2f}, {prob2:.2f}")
        return f'{prob1}/{prob2}'
    else:
        try:
            odds = int(odds.strip())
        except ValueError:
            print(f"Error: {odds} is not a valid integer.")
        if odds > 0:
            implied_prob = 100 / (odds + 100)
        else:
            implied_prob = abs(odds) / (abs(odds) + 100)
        print(f"Single implied probability for {odds}: {implied_prob:.2f}")
        return implied_prob


def american_to_decimal(odds):
    if odds > 0:
        return 1 + (odds / 100)
    else:
        return 1 + (100 / abs(odds))

def dejuice(probability, juice=0.06):
    if isinstance(probability, str) and '/' in probability:
        prob1, prob2 = map(float, probability.split('/'))

        total_prob = prob1 + prob2
        juice = total_prob - 1

        dejuiced_prob1 = prob1 / total_prob
        dejuiced_prob2 = prob2 / total_prob
        print(f"Dejuiced Probability for {prob1:.2f}/{prob2:.2f}: {dejuiced_prob1:.2f} @{juice} juice")
        return dejuiced_prob1
    else:
        dejuiced_prob = float(probability) / (1 + juice)
        print(f"Dejuiced Probability (single): {dejuiced_prob:.2f} @{juice} juice")
        return dejuiced_prob

def fv(dejuiced_probabilities):
    average_prob = sum(dejuiced_probabilities) / len(dejuiced_probabilities)
    print(f"Average Dejuiced Probability (Fair Value): {average_prob:.2f}")
    return average_prob

def ev(true_probability, your_decimal_odds):
    ev_value = true_probability * your_decimal_odds - 1
    print(f"EV Calculation: True Probability: {true_probability:.2f}, Your Decimal Odds: {your_decimal_odds:.2f}, EV: {ev_value:.2f}")
    return ev_value


def kelly(true_probability, your_decimal_odds, bankroll, unit_size):
    bankroll_units = bankroll // unit_size
    b = your_decimal_odds - 1
    p = true_probability
    q = 1 - p
    kelly_fraction = (b * p - q) / b
    kelly_fraction = max(kelly_fraction , 0)
    fractions = [1, 0.75, 0.5, 0.25]
    bet_sizes = {}
    for fraction in fractions:
        units_to_bet = kelly_fraction * bankroll_units * fraction
        bet_sizes[f"{int(fraction * 100)}% Kelly"] = units_to_bet
    return bet_sizes

def how_good(your_odds, other_odds, bankroll, unit_size, juice=0.06):
    results = []
    for odds in other_odds:
        if odds.startswith('avg(') and odds.endswith(')'):
            odds = odds[4:-1]
        odds = odds.split(', ')
        dejuiced_probabilities = []
        for item in odds:
            implied = implied_probability(item)
            dejuiced = dejuice(implied, juice)
            dejuiced_probabilities.append(dejuiced)
        true_probability = fv(dejuiced_probabilities)
        results.append(true_probability)
    true_probability = 1
    for result in results:
        true_probability *= result
    your_decimal_odds = american_to_decimal(your_odds)
    value = ev(true_probability, your_decimal_odds)
    units = kelly(true_probability, your_decimal_odds, bankroll, unit_size)
    return value, juice, units

def split_odds(odds):
    parts = re.split(r',\s*(?![^()]*\))', odds)
    return [part.strip() for part in parts]