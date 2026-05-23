import re

# Categorization rules dictionary mapping category names to lists of regex patterns or keywords.
# Order of matching is important: specific items (like Rent or Salary) are checked before generic ones (like UPI Transfers).
CATEGORY_RULES = [
    (
        "Salary",
        [
            r"\bsalary\b", r"\bsal\b", r"\bpayroll\b", r"\bcredit interest\b", 
            r"\bint\.rec\b", r"\binterest received\b", r"\bdividend\b", r"\bft - monthly salary\b"
        ]
    ),
    (
        "Rent",
        [
            r"\brent\b", r"\bhouse rent\b", r"\bpg rent\b", r"\bflat rent\b", r"\blandlord\b"
        ]
    ),
    (
        "EMI",
        [
            r"\bemi\b", r"\bloan\b", r"\bfinance\b", r"\bmortgage\b", r"\bbajaj\b", 
            r"\bhdfc loan\b", r"\bsbi loan\b", r"\blic\b", r"\bchg - emi\b"
        ]
    ),
    (
        "Subscriptions",
        [
            r"\bnetflix\b", r"\bspotify\b", r"\byoutube premium\b", r"\bprime video\b", 
            r"\bapple\.com\b", r"\bgoogle play\b", r"\bgithub\b", r"\bicloud\b"
        ]
    ),
    (
        "Entertainment",
        [
            r"\bbookmyshow\b", r"\bbms\b", r"\bpvr\b", r"\bcinepolis\b", r"\bmovies\b", 
            r"\bgaming\b", r"\bsteam\b", r"\bplaystation\b", r"\bhotstar\b", r"\bprime\b"
        ]
    ),
    (
        "Food",
        [
            r"\bswiggy\b", r"\bzomato\b", r"\brestaurant\b", r"\bcafe\b", r"\bfood\b", 
            r"\beats\b", r"\bmcdonalds\b", r"\bstarbucks\b", r"\bpizzahut\b", r"\bdominos\b", 
            r"\bbakery\b", r"\bdiner\b", r"\bburger\b", r"\bdining\b"
        ]
    ),
    (
        "Travel",
        [
            r"\buber\b", r"\bola\b", r"\bnamma\b", r"\bmetro\b", r"\birctc\b", 
            r"\bauto\b", r"\bfuel\b", r"\bpetrol\b", r"\bhpcl\b", r"\bbpcl\b", 
            r"\biocl\b", r"\bcab\b", r"\btravel\b", r"\bflight\b", r"\brailway\b", 
            r"\bmakemytrip\b", r"\beasemytrip\b"
        ]
    ),
    (
        "Utilities",
        [
            r"\belectricity\b", r"\bbescom\b", r"\bwater\b", r"\brecharge\b", r"\bjio\b", 
            r"\bairtel\b", r"\bbill\b", r"\bbsnl\b", r"\bvi \b", r"\bact fibernet\b", 
            r"\bgas\b", r"\bindane\b", r"\bhpgas\b", r"\bbroadband\b", r"\binsurance\b"
        ]
    ),
    (
        "Shopping",
        [
            r"\bamazon\b", r"\bflipkart\b", r"\bmyntra\b", r"\bretail\b", r"\bshopping\b", 
            r"\bgrocery\b", r"\bsupermarket\b", r"\bmart\b", r"\bbigbasket\b", r"\bblinkit\b", 
            r"\bzepto\b", r"\bdmart\b", r"\bjiomart\b", r"\bdecathlon\b", r"\bfashion\b", 
            r"\bnykaa\b", r"\bapparel\b"
        ]
    ),
    (
        "UPI Transfers",
        [
            r"\bupi\b", r"\bgpay\b", r"\bphonepe\b", r"\bpaytm\b", r"\bbhim\b", 
            r"\bp2p\b", r"\bpeer to peer\b", r"\btransfer to\b", r"\btransfer from\b"
        ]
    )
]

def categorize_transaction(narration: str) -> str:
    """
    Categorizes a transaction based on regular expression keywords.
    Returns the category string (e.g. 'Food', 'Travel') if matched, otherwise 'Others'.
    """
    narration_lower = narration.lower()
    
    for category, patterns in CATEGORY_RULES:
        for pattern in patterns:
            # Match word boundary or simple substring
            if re.search(pattern, narration_lower):
                return category
                
    return "Others"