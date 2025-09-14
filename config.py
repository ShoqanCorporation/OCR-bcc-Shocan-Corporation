import os


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "ВАШ_API_КЛЮЧ")
GEMINI_MODEL = "gemini-1.5-flash"


REQUIRED_FIELDS = [
    "document_type",
    "doc_id",
    "date",
    "payer_name",
    "beneficiary_name",
    "amount",
    "currency",
    "account_number",
    "iban"
]