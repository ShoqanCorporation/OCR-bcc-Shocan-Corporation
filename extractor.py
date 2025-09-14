import pandas as pd
import openpyxl
import fitz  # PyMuPDF
import io

from ocr_engine import run_ocr
from postprocess_gemini import ocr_to_json_with_gemini
from utils import load_image

def process_image(file_bytes, use_gemini):
    """Обрабатывает один файл изображения."""
    image_cv = load_image(file_bytes)
    merged_text, ocr_details = run_ocr(image_cv)
    if not merged_text.strip():
        return {"error": "No text detected"}, ocr_details, []
    
    extracted_data = ocr_to_json_with_gemini(merged_text) if use_gemini else {}
    return extracted_data, ocr_details, [image_cv]

def process_pdf(file_bytes, use_gemini):
    """Извлекает текст и изображения из PDF, затем обрабатывает."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    full_text = ""
    images_found = []
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        full_text += page.get_text("text") + "\n"
        
        for img_ref in page.get_images(full=True):
            xref = img_ref[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_cv = load_image(image_bytes)
            images_found.append(image_cv)
            
            ocr_text, _ = run_ocr(image_cv)
            full_text += ocr_text + "\n"
            
    if not full_text.strip():
        return {"error": "No text or images found in PDF"}, {}, images_found
        
    extracted_data = ocr_to_json_with_gemini(full_text) if use_gemini else {}
    ocr_details = {"merged_text": full_text}
    return extracted_data, ocr_details, images_found

def process_excel(file_bytes, use_gemini):
    """
    Извлекает текст и изображения из XLSX напрямую через openpyxl.
    """
    full_text = ""
    images_found = []
    
    # 1. Извлекаем текст из всех ячеек
    df = pd.read_excel(io.BytesIO(file_bytes))
    for col in df.columns:
        full_text += " ".join(df[col].dropna().astype(str)) + "\n"
        
    # 2. ✅ ИЗМЕНЕНИЕ: Извлекаем изображения напрямую
    wb = openpyxl.load_workbook(io.BytesIO(file_bytes))
    for sheet in wb.worksheets:
        for i, image in enumerate(sheet._images):
            print(f"Excel: Найдено изображение #{i+1} на листе '{sheet.title}'. Запускаем OCR...")
            # Изображения хранятся в байтах
            image_bytes = image.ref.getvalue()
            image_cv = load_image(image_bytes)
            images_found.append(image_cv)
            
            ocr_text, _ = run_ocr(image_cv)
            full_text += ocr_text + "\n"

    if not full_text.strip():
        return {"error": "No text or images found in Excel file"}, {}, images_found
        
    extracted_data = ocr_to_json_with_gemini(full_text) if use_gemini else {}
    ocr_details = {"merged_text": full_text}
    return extracted_data, ocr_details, images_found

def process_document(file_name, file_bytes, use_gemini):
    """Определяет тип файла и вызывает соответствующий обработчик."""
    file_ext = file_name.lower().split('.')[-1]
    if file_ext in ('png', 'jpg', 'jpeg'):
        return process_image(file_bytes, use_gemini)
    elif file_ext == 'pdf':
        return process_pdf(file_bytes, use_gemini)
    elif file_ext == 'xlsx':
        return process_excel(file_bytes, use_gemini)
    else:
        return {"error": "Unsupported file format"}, {}, []