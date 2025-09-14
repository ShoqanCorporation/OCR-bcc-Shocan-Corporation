from paddleocr import PaddleOCR
from utils import to_pil

paddle_model = PaddleOCR(use_angle_cls=True, lang='ru')

def ocr_paddle(image_cv):
    result = paddle_model.ocr(image_cv)

    if not result or not result[0]:
        print("DEBUG: PaddleOCR вернул пустой результат.")
        return []

    items = []
    data_from_ocr = result[0]

    if isinstance(data_from_ocr, dict) and 'rec_texts' in data_from_ocr:
        print("DEBUG: Обнаружен новый сложный формат результата.")
        texts = data_from_ocr.get('rec_texts', [])
        scores = data_from_ocr.get('rec_scores', [])
        boxes = data_from_ocr.get('rec_polys', [])

        for text, score, box in zip(texts, scores, boxes):
            items.append({"text": text, "confidence": float(score), "box": box})

    elif isinstance(data_from_ocr, list):
        print("DEBUG: Обнаружен стандартный формат результата (список).")
        for line in data_from_ocr:
            if not isinstance(line, list) or len(line) < 2:
                continue

            box = line[0]
            text_info = line[1]

            if isinstance(text_info, (list, tuple)) and len(text_info) == 2:
                text, score = text_info
            else:
                text = str(text_info)
                score = 0.5
            
            items.append({"text": str(text), "confidence": float(score), "box": box})

    if not items:
        print("DEBUG: Не удалось извлечь элементы из результата OCR.")
        
    return items

def run_ocr(image_cv):
    paddle_out = ocr_paddle(image_cv)
    merged_text = "\n".join([item['text'] for item in paddle_out])
    
    return merged_text, {"lines": paddle_out, "merged_text": merged_text}