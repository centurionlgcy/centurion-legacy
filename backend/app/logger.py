import csv
import os
from datetime import datetime

LOG_FILE = "signals_log.csv"

def log_signal(symbol, plan, signal_data):

    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "symbol",
                "plan",
                "signal",
                "confidence",
                "signal_strength"
            ])

        writer.writerow([
            datetime.utcnow().isoformat(),
            symbol,
            plan,
            signal_data.get("signal"),
            signal_data.get("confidence"),
            signal_data.get("signal_strength")
        ])
