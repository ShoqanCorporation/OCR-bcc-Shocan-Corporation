import re
import json
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL

if not GEMINI_API_KEY or GEMINI_API_KEY == "ВАШ_API_КЛЮЧ":
    raise ValueError("Укажите корректный GEMINI_API_KEY в config.py")
genai.configure(api_key=GEMINI_API_KEY)


def build_prompt(raw_json: str) -> str:
    """
    Строим строгий prompt для извлечения данных из Excel-подобного JSON.
    """
    prompt = f"""
You are a data extraction system. 
Your task is to convert messy OCR/Excel-like JSON with document fields into a clean normalized JSON object.

⚠️ Return ONLY a valid JSON, no explanations, no extra text.

The JSON must have this exact structure:

{{
  "contract": {{
    "file_name": "...",
    "contract_number": "...",
    "contract_date": "YYYY-MM-DD",
    "contract_end_date": "YYYY-MM-DD",
    "beneficiary": {{
      "name": "...",
      "country": "...",
      "country_code": "..."
    }},
    "counterparty": {{
      "name": "..."
    }},
    "amount": {{
      "value": 0,
      "currency_contract": "...",
      "currency_payment": "..."
    }},
    "terms": {{
      "validity": "...",
      "payment": "..."
    }}
  }},
  "bank_details": {{
    "recipient_bank": {{
      "name": "...",
      "address": "...",
      "yhii": "...",
      "swift": "...",
      "account": "...",
      "kio_code": "...",
      "iban": "..."
    }},
    "correspondent_bank": {{
      "name": "...",
      "address": "...",
      "swift": "...",
      "bic": "...",
      "inn": "...",
      "kpp": "...",
      "account": "..."
    }}
  }},
  "payment_purpose": "..."
}}

Input (messy Excel-like JSON):
{raw_json}

Now return ONLY the cleaned JSON in the required structure.
"""
    return prompt


def ocr_to_json_with_gemini(raw_json: str) -> dict:
    """
    Отправляет JSON из Excel/документа в Gemini и возвращает нормализованный JSON.
    """
    prompt = build_prompt(raw_json)
    model = genai.GenerativeModel(GEMINI_MODEL)

    try:
        generation_config = genai.types.GenerationConfig(
            temperature=0.0,
            response_mime_type="application/json"
        )

        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )

        return json.loads(response.text)

    except Exception as e:
        print(f"Ошибка при запросе к Gemini API: {e}")
        return {"error": f"API call failed: {e}"}


# Тест
if __name__ == "__main__":
    messy_input = '''{"sheets":[{"name":"Sheet1","data":[["Название файла","8A16"],["Реквизиты","контракта","дата заключения","..."]]}]}'''
    result = ocr_to_json_with_gemini(messy_input)
    print(json.dumps(result, ensure_ascii=False, indent=2))
