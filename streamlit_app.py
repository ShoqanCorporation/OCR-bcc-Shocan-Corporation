import streamlit as st
import json
from extractor import process_document # Изменили импорт
from validator import validate_date, validate_amount
import cv2

st.set_page_config(page_title="Универсальный OCR 2.0", layout="wide")
st.title("🚀 Универсальный OCR 2.0 для Документов")

uploaded_file = st.file_uploader(
    "Загрузите документ (JPG, PNG, PDF, XLSX)", 
    type=["png", "jpg", "jpeg", "pdf", "xlsx"]
)
use_gemini_checkbox = st.checkbox("Использовать Gemini для извлечения данных", value=True)

if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()
    file_name = uploaded_file.name
    
    col1, col2 = st.columns(2)
    
    with col2:
        with st.spinner("Анализ документа..."):

            extracted_data, ocr_details, images_found = process_document(file_name, file_bytes, use_gemini_checkbox)
            
            st.subheader("Полный извлечённый текст (digital + OCR)")
            st.text_area("Merged Text", ocr_details.get("merged_text", ""), height=250)
            
            st.subheader("Извлечённые поля (JSON)")
            st.json(extracted_data)

            st.subheader("Валидация полей")
            if extracted_data and "error" not in extracted_data:
                st.info(f"Дата: {validate_date(extracted_data.get('date'))}")
                st.info(f"Сумма: {validate_amount(extracted_data.get('amount'))}")
            else:
                st.error("Извлечение не удалось, валидация невозможна.")

    with col1:
        st.subheader("Предпросмотр документа")
        # Отображаем первую страницу PDF или найденные картинки
        if file_name.lower().endswith('.pdf'):
            st.success(f"Загружен PDF-файл: {file_name}")
            st.write("Найденные изображения (если есть):")
        elif file_name.lower().endswith('.xlsx'):
            st.success(f"Загружен Excel-файл: {file_name}")
            st.write("Найденные изображения (если есть):")
        
        if images_found:
            for i, img_cv in enumerate(images_found):
                st.image(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB), caption=f"Изображение {i+1}")
        elif file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
             st.image(file_bytes, caption="Загруженное изображение")
        else:
            st.info("Предпросмотр изображений для этого файла недоступен.")