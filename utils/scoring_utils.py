import math


def count_score(directions):
    """
    Returns a count score for In and Out directions.
    """
    return {
        "In": sum(1 for d in directions if d == "In"),
        "Out": sum(1 for d in directions if d == "Out")
    }

def rssi_single_score(rssi):
    """
    Converts RSSI value into a score based on signal strength.
    """
    if rssi <= -80:
        return 0
    elif rssi < -55:
        return ((rssi + 80) / 25) * 5
    else:
        delta = rssi + 55
        return min(5 + 10 * (1 - math.exp(-0.15 * delta)), 15)

def rssi_score_by_direction(history):
    """
    Extracts and ranks highest RSSI score by direction from recent history.
    """
    scores = {"In": 0, "Out": 0}
    for direction in scores:
        rssis = [rssi_single_score(e['rssi']) for e in history if e['direction'] == direction]
        if rssis:
            scores[direction] = sorted(rssis, reverse=True)[0]
    return scores

def trend_score(history):
    """
    Analyzes RSSI trend over time to detect increasing signal strength.
    """
    scores = {"In": 0, "Out": 0}
    for direction in scores:
        rssi_seq = [e['rssi'] for e in history if e['direction'] == direction]
        if len(rssi_seq) >= 2:
            inc_count = sum(1 for i in range(1, len(rssi_seq)) if rssi_seq[i] > rssi_seq[i - 1])
            scores[direction] = round((inc_count / (len(rssi_seq) - 1)) * 10, 2)
    return scores

def time_score(ms):
    """
    Calculates a weighted score based on how long since last same-direction scan.
    """
    if ms < 5000:
        return 0
    elif ms < 120000:
        return (ms - 5000) / 115000 * 3
    delta_sec = (ms - 120000) / 1000
    return 3 + 2 * min(math.log1p(delta_sec), math.log1p(600)) / math.log1p(600)

def time_score_by_direction(history, current_time):
    """
    Looks back for the most recent same-direction event and scores time gap.
    """
    scores = {"In": 0, "Out": 0}
    for direction in scores:
        for e in reversed(history):
            if e['direction'] == direction:
                scores[direction] = time_score(current_time - e['tagtime'])
                break
    return scores