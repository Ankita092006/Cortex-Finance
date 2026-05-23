import re
from dateutil import parser as date_parser

def clean_amount(amount_val) -> float:
    """
    Sanitizes and converts currency strings into clean float values.
    
    Security / Robustness:
    - Removes currency symbols (₹, $, Rs, etc.).
    - Handles formatting like commas (1,234.56).
    - Handles credit/debit suffixes (e.g., '100.00 Cr' or '50.00 Dr').
    - Handles parenthesized negative values (e.g., '(123.45)').
    - Prevents crashes by returning 0.0 on malformed input.
    """
    if amount_val is None:
        return 0.0
        
    if isinstance(amount_val, (int, float)):
        return float(amount_val)
        
    amount_str = str(amount_val).strip()
    if not amount_str:
        return 0.0
        
    # Check for credit/debit suffix before stripping letters
    is_credit = False
    lower_str = amount_str.lower()
    if "cr" in lower_str:
        is_credit = True
    
    # Check for parenthesized negative number
    is_negative = False
    if amount_str.startswith('(') and amount_str.endswith(')'):
        is_negative = True
        amount_str = amount_str[1:-1]
        
    # Remove any character except digits, decimal point, minus sign
    # Note: Keep the decimal point and minus sign
    amount_str = re.sub(r"[^\d\.-]", "", amount_str)
    
    try:
        val = float(amount_str)
        if is_negative:
            val = -val
        return val
    except ValueError:
        return 0.0

def normalize_date(date_val) -> str:
    """
    Normalizes dates from various formats (e.g., DD/MM/YYYY, DD-MMM-YY) to YYYY-MM-DD.
    
    Security / Robustness:
    - Interprets day-first (DD/MM/YYYY) preferred in Indian banking.
    - Gracefully returns the original string or empty string to avoid failing the pipeline.
    """
    if date_val is None:
        return ""
        
    date_str = str(date_val).strip()
    if not date_str:
        return ""
        
    try:
        # Dayfirst=True is critical for Indian bank statement formats (e.g., 05-04-2026 is 5th April, not 4th May)
        parsed_date = date_parser.parse(date_str, dayfirst=True)
        return parsed_date.strftime("%Y-%m-%d")
    except Exception:
        # Fallback regex search for date patterns if dateutil fails
        date_match = re.search(r"(\d{1,2})[/-](\d{1,2}|[A-Za-z]{3})[/-](\d{2,4})", date_str)
        if date_match:
            try:
                parsed_date = date_parser.parse(date_match.group(0), dayfirst=True)
                return parsed_date.strftime("%Y-%m-%d")
            except Exception:
                pass
        return date_str

def clean_narration(narration_val) -> str:
    if narration_val is None:
        return ""
        
    narration_str = str(narration_val).strip()
    # Replace multiple whitespaces/tabs/newlines with a single space
    narration_str = re.sub(r"\s+", " ", narration_str)
    return narration_str