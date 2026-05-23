from datetime import datetime
from collections import defaultdict

def parse_date(date_val) -> datetime:
    """Parses a date string or object into a datetime object."""
    if isinstance(date_val, datetime):
        return date_val
    # If it is a date object
    if hasattr(date_val, "strftime") and not hasattr(date_val, "hour"):
        return datetime(date_val.year, date_val.month, date_val.day)
        
    date_str = str(date_val).strip()
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d", "%d/%m/%Y", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(date_str.split()[0], fmt)
        except ValueError:
            continue
    raise ValueError(f"Could not parse date format: {date_val}")

def detect_recurring_payments(transactions: list[dict]) -> list[dict]:
    """
    Identifies recurring transactions (e.g., subscriptions, EMIs, salaries) 
    based on regularity of date intervals and merchant narrations.
    
    Returns a list of dictionaries, where each dictionary represents a detected 
    recurring pattern (merchant, frequency, average amount, occurrences).
    """
    if not transactions:
        return []

    # Group transactions by cleaned narration
    groups = defaultdict(list)
    for tx in transactions:
        narration = tx.get("narration", "").strip()
        if not narration:
            continue
        try:
            dt = parse_date(tx.get("date"))
            amt = abs(float(tx.get("amount", 0)))
            groups[narration].append({
                "date": dt,
                "amount": amt,
                "original": tx
            })
        except Exception:
            continue

    recurring_patterns = []

    for narration, txs in groups.items():
        if len(txs) < 2:
            continue

        # Sort by date
        txs.sort(key=lambda x: x["date"])

        # Calculate differences in days
        intervals = []
        for i in range(1, len(txs)):
            diff = (txs[i]["date"] - txs[i-1]["date"]).days
            intervals.append(diff)

        # Check if intervals correspond to standard frequencies:
        # - Weekly: ~7 days (range: 5-9 days)
        # - Bi-weekly: ~14 days (range: 12-16 days)
        # - Monthly: ~30 days (range: 25-35 days)
        
        # We check the median or mean interval
        mean_interval = sum(intervals) / len(intervals)
        
        # Check standard deviation of intervals to check regularity
        variance = sum((x - mean_interval) ** 2 for x in intervals) / len(intervals)
        std_dev = variance ** 0.5

        # Check amount consistency
        amounts = [x["amount"] for x in txs]
        avg_amount = sum(amounts) / len(amounts)
        amount_variance = sum((x - avg_amount) ** 2 for x in amounts) / len(amounts)
        amount_std_dev = amount_variance ** 0.5
        
        # We classify frequency
        frequency = None
        if 5 <= mean_interval <= 9 and std_dev <= 2.0:
            frequency = "Weekly"
        elif 12 <= mean_interval <= 16 and std_dev <= 3.0:
            frequency = "Bi-weekly"
        elif 25 <= mean_interval <= 35 and std_dev <= 5.0:
            frequency = "Monthly"

        # If a matching frequency is found, flag it
        if frequency:
            recurring_patterns.append({
                "narration": narration,
                "frequency": frequency,
                "average_amount": round(avg_amount, 2),
                "occurrences": len(txs),
                "last_date": txs[-1]["date"].strftime("%Y-%m-%d"),
                "is_fixed_amount": amount_std_dev < (avg_amount * 0.05)  # Less than 5% variance in amount
            })

    return recurring_patterns
