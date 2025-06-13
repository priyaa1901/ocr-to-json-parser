import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import re
from langdetect import detect



LANGUAGE_MAP = {
    'en': 'eng',
    'fr': 'fra',
    'de': 'deu',
}


def load_image_from_upload(file_path):
    if file_path.lower().endswith('.pdf'):
        return convert_from_path(file_path, dpi=300)  # better OCR quality
    else:
        return [Image.open(file_path)]


def normalize_numbered_points(text):
    text = re.sub(r'\b[lI]\b[\.:\s]?', '1. ', text)
    text = re.sub(r'\b(\d{1,2})(\s+)([A-ZÉÈÇa-zéèêàç])', r'\1. \3', text)
    return text

def extract_text(image):
    raw_text = pytesseract.image_to_string(image)

    try:
        lang_detected = detect(raw_text)
        lang_code = LANGUAGE_MAP.get(lang_detected, 'eng')
    except:
        lang_code = 'eng'

    config = r'--oem 1 --psm 6'
    final_text = pytesseract.image_to_string(image, lang=lang_code, config=config)

    return normalize_numbered_points(final_text)


def clean_text(text):
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    return text


def extract_key_values(text):
    key_values = {}
    patterns = {
        'invoice_number': r'(invoice number|inv#|invoice no)[:\s]*([\w-]+)',
        'date': r'(date)[:\s]*([\d]{2,4}[-/][\d]{1,2}[-/][\d]{1,4})',
        'total': r'(total amount|total)[:\s]*([$₹]?\d+[\.,]?\d*)',
        'email': r'([\w\.-]+@[\w\.-]+\.\w+)',
        'phone': r'(\+?\d[\d\s\-]{9,})'
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            key_values[key] = match.group(1)
    return key_values

# Final JSON result
def structure_to_json(text):
    key_values = extract_key_values(text)
    result = {"text": text}
    if key_values:
        result["key_values"] = key_values
    return result
