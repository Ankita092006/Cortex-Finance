import pandas as pd
from app.services.cleaner import clean_amount, normalize_date, clean_narration

def map_csv_headers(columns):
    """Maps columns of a CSV to transaction attributes dynamically."""
    mapping = {}
    for i, col in enumerate(columns):
        c = str(col).lower().strip()
        if "date" in c:
            if "val" not in c or "date" not in mapping:
                mapping["date"] = col
        elif any(k in c for k in ["narration", "particulars", "description", "remarks"]):
            mapping["narration"] = col
        elif any(k in c for k in ["withdrawal", "debit", "dr"]):
            mapping["debit"] = col
        elif any(k in c for k in ["deposit", "credit", "cr"]):
            mapping["credit"] = col
        elif "amount" in c:
            if "debit" in c or "dr" in c:
                mapping["debit"] = col
            elif "credit" in c or "cr" in c:
                mapping["credit"] = col
            else:
                mapping["amount"] = col
        elif any(k in c for k in ["balance", "bal"]):
            mapping["balance"] = col
    return mapping

def extract_transactions_csv(csv_path: str) -> list:
    """
    Parses a CSV bank statement, cleans row fields, and maps values.
    """
    transactions = []
    try:
        # Load CSV, try standard encoding first, fallback to ISO-8859-1 for Excel-compatible exports
        try:
            df = pd.read_csv(csv_path)
        except UnicodeDecodeError:
            df = pd.read_csv(csv_path, encoding="ISO-8859-1")
            
        # Clean column names
        df.columns = [str(c).strip() for c in df.columns]
        
        # Check for column mapping
        mapping = map_csv_headers(df.columns)
        
        # We need at least date and narration to identify transactions
        if "date" not in mapping or "narration" not in mapping:
            return []
            
        date_col = mapping["date"]
        narration_col = mapping["narration"]
        debit_col = mapping.get("debit")
        credit_col = mapping.get("credit")
        amount_col = mapping.get("amount")
        balance_col = mapping.get("balance")
        
        # Drop rows where date or narration is null
        df = df.dropna(subset=[date_col, narration_col])
        
        for _, row in df.iterrows():
            date_val = str(row[date_col]).strip()
            narration_val = str(row[narration_col]).strip()
            
            if not date_val or date_val.lower() == "nan" or not narration_val or narration_val.lower() == "nan":
                continue
                
            balance = clean_amount(row[balance_col]) if balance_col else 0.0
            debit = 0.0
            credit = 0.0
            
            if debit_col and credit_col:
                debit = clean_amount(row[debit_col])
                credit = clean_amount(row[credit_col])
            elif amount_col:
                amt = clean_amount(row[amount_col])
                row_str = " ".join([str(x) for x in row.values]).lower()
                if "cr" in row_str or "credit" in row_str:
                    credit = amt
                else:
                    debit = amt
            
            transactions.append({
                "date": normalize_date(date_val),
                "narration": clean_narration(narration_val),
                "debit": debit,
                "credit": credit,
                "balance": balance
            })
            
    except Exception as e:
        print(f"Error parsing CSV statement: {e}")
        
    return transactions
