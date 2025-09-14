import cv2
import numpy as np
from PIL import Image

def load_image(input_path_or_bytes):
    """Загружает изображение из пути к файлу или из байтов."""
    if isinstance(input_path_or_bytes, str):
        img = cv2.imdecode(np.fromfile(input_path_or_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
    elif isinstance(input_path_or_bytes, bytes):
        img = cv2.imdecode(np.frombuffer(input_path_or_bytes, np.uint8), cv2.IMREAD_COLOR)
    else:
        raise ValueError("Unsupported input type for load_image")
    return img

def to_pil(cv_img):
    """Конвертирует изображение из OpenCV (BGR) в PIL (RGB)."""
    return Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))