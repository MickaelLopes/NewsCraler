import re

def _match_name_regex(first_name : str , last_name: str, text : str):
    # First regex with [first] (,) [Last] : e.g. John Smith
    regex1 = re.compile(rf"\b({first_name})\b\s*\,?\s*\b({last_name})\b", re.IGNORECASE)
    # Second regex with [last] (,) [first] : e.g. Smith, John
    regex2 = re.compile(rf"\b({last_name})\b\s*\,?\s*\b({first_name})\b", re.IGNORECASE)

    for reg in [regex1,regex2]: 
        match = reg.search(text, re.IGNORECASE)
        if match :
            # if match one of the regex 
            return True
    # If no match on both regex
    return False 