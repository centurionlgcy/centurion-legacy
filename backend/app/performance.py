import csv
from collections import Counter

LOG_FILE = "signals_log.csv"

def calculate_performance():

    try:
        with open(LOG_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

    except FileNotFoundError:
        return {"error": "No log data available yet."}

    total_signals = len(rows)

    if total_signals == 0:
        return {"error": "Log file is empty."}

    plan_counts = Counter(row["plan"] for row in rows)
    signal_counts = Counter(row["signal"] for row in rows)
    strength_counts = Counter(row["signal_strength"] for row in rows)

    avg_confidence = round(
        sum(float(row["confidence"]) for row in rows) / total_signals,
        2
    )

    return {
        "total_signals": total_signals,
        "plans_distribution": dict(plan_counts),
        "signal_distribution": dict(signal_counts),
        "strength_distribution": dict(strength_counts),
        "average_confidence": avg_confidence
    }
