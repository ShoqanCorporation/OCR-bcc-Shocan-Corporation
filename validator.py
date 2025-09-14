import re
from datetime import datetime

def validate_date(date_str):
    """Проверяет и форматирует дату."""
    if not date_str:
        return "Missing"
    for fmt in ("%d.%m.%Y", "%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y", "%d.%m.%y"):
        try:
            valid_date = datetime.strptime(date_str, fmt)
            return f"Valid ({valid_date.strftime('%Y-%m-%d')})"
        except (ValueError, TypeError):
            continue
    return "Invalid Format"

def validate_amount(amount_obj):
    """Проверяет сумму."""
    if not isinstance(amount_obj, dict) or 'value' not in amount_obj:
        return "Missing"
    try:
        value = float(amount_obj['value'])
        return f"Valid ({value})"
    except (ValueError, TypeError):
        return "Invalid Value"