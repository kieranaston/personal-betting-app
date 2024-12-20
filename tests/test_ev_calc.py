import betting_app.ev_calc as ev_calc

def test_implied_probability_valid():
    odds_1 = '150'
    odds_2 = '-150'
    odds_3 = '150/-150'
    odds_4 = '-150/150'
    result_1 = ev_calc.implied_probability(odds_1)
    result_2 = ev_calc.implied_probability(odds_2)
    result_3 = ev_calc.implied_probability(odds_3)
    result_4 = ev_calc.implied_probability(odds_4)
    assert result_1 == 0.4
    assert result_2 == 0.6
    assert result_3 == '0.4/0.6'
    assert result_4 == '0.6/0.4'

def test_implied_probability_invalid():
    odds = 'invalid'
    result = ev_calc.implied_probability(odds)
    assert result == 'Invalid odds format.'

def test_american_to_decimal_valid():
    odds = 150
    result = ev_calc.american_to_decimal(odds)
    assert result == 2.5
    odds_2 = -150
    result = ev_calc.american_to_decimal(odds_2)
    assert round(result, 2) == 1.67

def test_dejuice_valid():
    probability = 0.67
    result = ev_calc.dejuice(probability)
    assert round(result, 4) == 0.6321
    probability_2 = '0.53'
    result = ev_calc.dejuice(probability_2, 0.045)
    assert round(result, 4) == 0.5072
    probability_3 = '0.4/0.8'
    result = ev_calc.dejuice(probability_3)
    assert round(result, 4) == 0.3333

def test_how_good():
    results = ev_calc.how_good(150, ['avg(-120, -110, -125)'],
                               100, 1)
    assert round(results[0], 2) == 0.28
