import pdfplumber
import re
from app.services.cleaner import clean_amount, normalize_date, clean_narration

def is_transaction_line(line: str) -> bool:
    """Checks if a text line starts with a date pattern, typical of a transaction."""
    # Matches patterns like DD/MM/YYYY, DD-MM-YYYY, DD-MMM-YYYY, DD-MMM-YY, etc.
    pattern = r"^\s*\d{1,2}[/-](\d{1,2}|[A-Za-z]{3})[/-]\d{2,4}"
    return bool(re.match(pattern, line))

def parse_text_line_fallback(line: str):
    """
    Fallback parser that processes a raw line of text.
    Uses regex to extract dates, narrations, debits/credits, and balance.
    """
    try:
        parts = line.split()
        if len(parts) < 3:
            return None

        # Extract date
        date = parts[0]
        
        # Balance is usually the last number in the line
        balance = clean_amount(parts[-1])
        
        # Simple heuristics for parsing amounts in space-delimited text
        debit = 0.0
        credit = 0.0
        
        # Look for numbers from the end
        numbers = []
        for p in reversed(parts[1:]):
            cleaned = re.sub(r"[^\d\.-]", "", p)
            if cleaned:
                try:
                    numbers.append((p, float(cleaned)))
                except ValueError:
                    pass
        
        # We need at least balance and transaction amount
        if len(numbers) >= 2:
            amount_str, amount_val = numbers[1] # second from last is transaction amount
            
            # Narration is everything between date and the numeric values
            amount_idx = parts.index(amount_str) if amount_str in parts else len(parts) - 2
            narration = " ".join(parts[1:amount_idx])
            
            # Check debit/credit indicators
            line_lower = line.lower()
            if "cr" in line_lower or "credit" in line_lower or "dep" in line_lower:
                credit = amount_val
            else:
                debit = amount_val
        else:
            # Fallback if numbers cannot be parsed properly
            narration = " ".join(parts[1:-1])
            debit = clean_amount(parts[-2]) if len(parts) > 2 else 0.0
            
        return {
            "date": normalize_date(date),
            "narration": clean_narration(narration),
            "debit": debit,
            "credit": credit,
            "balance": balance
        }
    except Exception:
        return None

def map_headers(row):
    """Maps row indices to transaction fields dynamically based on column headers."""
    mapping = {}
    for i, cell in enumerate(row):
        if not cell:
            continue
        c = str(cell).lower().strip()
        if "date" in c:
            if "val" not in c or "date" not in mapping:
                mapping["date"] = i
        elif any(k in c for k in ["narration", "particulars", "description", "remarks"]):
            mapping["narration"] = i
        elif any(k in c for k in ["withdrawal", "debit", "dr"]):
            mapping["debit"] = i
        elif any(k in c for k in ["deposit", "credit", "cr"]):
            mapping["credit"] = i
        elif "amount" in c:
            if "debit" in c or "dr" in c:
                mapping["debit"] = i
            elif "credit" in c or "cr" in c:
                mapping["credit"] = i
            else:
                mapping["amount"] = i
        elif any(k in c for k in ["balance", "bal"]):
            mapping["balance"] = i
    return mapping

def parse_table_row(row, mapping):
    """Parses a list of table cell strings using column mapping indices."""
    try:
        date_idx = mapping.get("date")
        narration_idx = mapping.get("narration")
        debit_idx = mapping.get("debit")
        credit_idx = mapping.get("credit")
        amount_idx = mapping.get("amount")
        balance_idx = mapping.get("balance")

        # Must have at least a date and narration to be a valid transaction
        if date_idx is None or narration_idx is None:
            return None

        date_val = row[date_idx]
        narration_val = row[narration_idx]
        
        # Verify date format looks like a date
        if not date_val or not is_transaction_line(str(date_val)):
            return None

        # Parse amounts
        balance = clean_amount(row[balance_idx]) if balance_idx is not None else 0.0
        debit = 0.0
        credit = 0.0

        if debit_idx is not None and credit_idx is not None:
            debit = clean_amount(row[debit_idx])
            credit = clean_amount(row[credit_idx])
        elif amount_idx is not None:
            amt = clean_amount(row[amount_idx])
            row_str = " ".join([str(x) for x in row]).lower()
            if "cr" in row_str or "credit" in row_str:
                credit = amt
            else:
                debit = amt

        return {
            "date": normalize_date(date_val),
            "narration": clean_narration(narration_val),
            "debit": debit,
            "credit": credit,
            "balance": balance
        }
    except Exception:
        return None

def extract_transactions(pdf_path: str) -> list:
    """
    Extracts transactions from a PDF statement using structured tables or line text fallback.
    """
    transactions = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # 1. Try structured table extraction
            tables = page.extract_tables()
            table_parsed = False
            
            if tables:
                for table in tables:
                    if len(table) < 2:
                        continue
                        
                    # Find header row to map columns
                    mapping = {}
                    header_row_idx = -1
                    
                    for r_idx, row in enumerate(table[:3]):  # check first 3 rows for headers
                        temp_map = map_headers(row)
                        if "date" in temp_map and "narration" in temp_map:
                            mapping = temp_map
                            header_row_idx = r_idx
                            break
                            
                    if mapping:
                        table_parsed = True
                        for row in table[header_row_idx + 1:]:
                            # Make sure row size matches mapping indices
                            if len(row) > max(mapping.values()):
                                tx = parse_table_row(row, mapping)
                                if tx:
                                    transactions.append(tx)
            
            # 2. Fall back to regex line-by-line parsing if table parsing was unsuccessful
            if not table_parsed:
                text = page.extract_text()
                if not text:
                    continue
                    
                lines = text.split("\n")
                for line in lines:
                    if is_transaction_line(line):
                        tx = parse_text_line_fallback(line)
                        if tx:
                            transactions.append(tx)
                            
    return transactions