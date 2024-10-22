import re

# Determines the implied probability from American odds
def implied_probability(odds):
    if '/' in odds:  # Check if two-legged odds are given
        side1, side2 = odds.split('/')
        side1 = int(side1.strip())
        side2 = int(side2.strip())

        # Calculate implied probabilities for both sides
        prob1 = 100 / (side1 + 100) if side1 > 0 else abs(side1) / (abs(side1) + 100)
        prob2 = 100 / (side2 + 100) if side2 > 0 else abs(side2) / (abs(side2) + 100)

        return f'{round(prob1, 4)}/{round(prob2, 4)}'  # Return as a string with both probabilities
    else:  # Single side odds
        try:
            odds = int(odds.strip())  # .strip() removes any surrounding whitespace
        except ValueError:
            print(f"Error: {odds} is not a valid integer.")
        if odds > 0:
            return round(100 / (odds + 100), 4)
        else:
            return round(abs(odds) / (abs(odds) + 100), 4)

'''
def implied_probability(odds):
    if odds > 0:
        return 100 / (odds + 100)
    else:
        return abs(odds) / (abs(odds) + 100)
'''
# Converts American odds to decimal odds
def american_to_decimal(odds):
    if odds > 0:
        return 1 + (odds / 100)
    else:
        return 1 + (100 / abs(odds))

# Dejuice with a standard margin of 6% (difficult to obtain both sides of a line for most bets)
def dejuice(probability, juice=0.06):  # Default juice to 6% if not provided
    if isinstance(probability, str) and '/' in probability:  # Two-sided odds
        prob1, prob2 = map(float, probability.split('/'))

        # Sum of probabilities gives us the bookmaker's margin (including juice)
        total_prob = prob1 + prob2

        # Calculate how much juice is in the market
        juice = total_prob - 1

        # Remove the juice proportionally from both sides
        dejuiced_prob1 = prob1 / total_prob
        dejuiced_prob2 = prob2 / total_prob

        return round(dejuiced_prob1, 4)
    else:  # Single probability
        dejuiced_prob = float(probability) / (1 + juice)
        return round(dejuiced_prob, 4)
'''
def dejuice(probability, juice):
    return probability / (1 + juice)
'''
# Average out dejuiced probabilities to approximate actual probability
def fv(dejuiced_probabilities):
    return sum(dejuiced_probabilities) / len(dejuiced_probabilities)

# Calculates expected value of your bet
def ev(true_probability, your_decimal_odds):
    return true_probability*your_decimal_odds - 1

# Determines unit size for bet using Kelly criterion
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

# Uses the other functions defined above to determine the ev using the odds you have and other books' odds
'''
def how_good(your_odds, other_odds, bankroll, unit_size, juice=0.06):
    dejuiced_probabilities = []
    for odds in other_odds:
        implied = implied_probability(odds)
        dejuiced = dejuice(implied, juice)
        dejuiced_probabilities.append(dejuiced)
    true_probability = fv(dejuiced_probabilities)
    your_decimal_odds = american_to_decimal(your_odds)
    value = ev(true_probability, your_decimal_odds)
    units = kelly(true_probability, your_decimal_odds, bankroll, unit_size)
    return value, juice, units
'''

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