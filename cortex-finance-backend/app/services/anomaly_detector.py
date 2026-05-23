import math

def detect_anomalies(transactions: list[dict], threshold_z: float = 2.0, min_amount: float = 10000.0) -> list[dict]:
    """
    Detects financial anomalies (outliers) in a list of transactions.
    
    Parameters:
    - transactions: List of transaction dicts (must contain 'amount' and 'narration').
    - threshold_z: Z-score threshold to classify as an anomaly (default: 2.0).
    - min_amount: The minimum amount (in INR) below which a transaction is never 
                  flagged as an anomaly to prevent flagging small expenses.
                  
    Returns:
    - List of transaction dicts flagged as anomalies, annotated with 'z_score' and 'anomaly_reason'.
    """
    if not transactions:
        return []

    # Filter transactions with valid amounts
    valid_txs = []
    for tx in transactions:
        try:
            amt = abs(float(tx.get("amount", 0)))
            valid_txs.append((tx, amt))
        except (ValueError, TypeError):
            continue

    if not valid_txs:
        return []

    n = len(valid_txs)
    amounts = [amt for _, amt in valid_txs]

    anomalies = []

    if n < 3:
        # For very small sets, use a flat relative threshold (e.g. 3x the median/average or static threshold)
        avg = sum(amounts) / n
        for tx, amt in valid_txs:
            if amt > min_amount and amt > 3 * avg:
                tx_copy = tx.copy()
                tx_copy["z_score"] = 0.0
                tx_copy["anomaly_reason"] = f"Amount ({amt}) is significantly higher than the average ({avg:.2f}) in a small sample."
                anomalies.append(tx_copy)
        return anomalies

    # Calculate Mean
    mean = sum(amounts) / n

    # Calculate Standard Deviation
    variance = sum((x - mean) ** 2 for x in amounts) / n
    std_dev = math.sqrt(variance)

    # Detect anomalies
    for tx, amt in valid_txs:
        if amt < min_amount:
            continue
            
        if std_dev > 0:
            z_score = (amt - mean) / std_dev
            if z_score > threshold_z:
                tx_copy = tx.copy()
                tx_copy["z_score"] = round(z_score, 2)
                tx_copy["anomaly_reason"] = f"Z-score of {z_score:.2f} exceeds threshold {threshold_z}. Mean: {mean:.2f}, Std Dev: {std_dev:.2f}."
                anomalies.append(tx_copy)
        else:
            # If standard deviation is 0, all amounts are identical; no anomalies.
            pass

    return anomalies
