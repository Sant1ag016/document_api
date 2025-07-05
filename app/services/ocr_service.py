from pdf2image import convert_from_bytes  # Necesitas instalar con: pip install pdf2image
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import io
import base64
import re
import unicodedata
import PyPDF2

# ───── Utilidades ─────

def decode_base64(base64_data):
    return base64.b64decode(base64_data)

def normalize_text(txt):
    return ''.join(c for c in unicodedata.normalize('NFD', txt)
                   if unicodedata.category(c) != 'Mn').lower()

# ───── Preprocesamiento de imagen ─────

def preprocess_image(image):
    img = image.convert("L")
    img = img.filter(ImageFilter.MedianFilter())
    img = ImageEnhance.Contrast(img).enhance(1.1)
    img = ImageEnhance.Brightness(img).enhance(1.2)
    return img

# ───── OCR ─────

TESSERACT_CONFIG = (
    "--oem 3 --psm 6 "
    "-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    "ÁÉÍÓÚÑáéíóúñ"
    "0123456789:/\\-."
)

def extract_text_from_image(image_data):
    img = preprocess_image(Image.open(io.BytesIO(image_data)))
    return pytesseract.image_to_string(img, config=TESSERACT_CONFIG)

# ───── Extracción de texto de PDF ─────

def extract_text_from_pdf(pdf_data):
    # Primero intentamos extraer texto nativo
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_data))
        text = ''
        for page in reader.pages:
            page_text = page.extract_text() or ''
            text += page_text + '\n'
        # Si hay texto significativo, lo retornamos
        if len(text.strip()) > 50:
            return text
    except Exception:
        text = ''
    # Si no se extrajo texto o es muy corto, caemos a OCR de imágenes
    try:
        images = convert_from_bytes(pdf_data, dpi=300)
        ocr_text = ''
        for img in images:
            img = preprocess_image(img)
            ocr_text += pytesseract.image_to_string(img, config=TESSERACT_CONFIG) + '\n'
        return ocr_text
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return ''

# ───── Validación de tipo de documento ─────

def validate_document_type(text):
    normalized = normalize_text(text)
    if "nuip" in normalized:
        return "Cédula de Ciudadanía digital"
    if "cedula" in normalized and "ciudadania" in normalized:
        if "numero" in normalized or re.search(r'\bno\.?\b', normalized):
            return "Cédula de Ciudadanía amarilla"
        return "Cédula de Ciudadanía"
    if "cedula de extranjeria" in normalized:
        return "Cédula de Extranjería"
    if "pasaporte" in normalized:
        return "Pasaporte"
    if any(k in normalized for k in ["identificacion", "documento de identidad", "id"]):
        return "Cédula"
    return "Unknown"

# ───── Extracción de campos ─────

GENERIC_FIELDS = {
    "first_name": [r"nombre[s]?", r"names?"],
    "last_name": [r"apellido[s]?", r"surnames?", r"last name"],
    "document_number": [r"nuip", r"no\.?", r"número", r"number", r"id"],
    "birth_date": [r"fecha de nacimiento", r"birth date"],
    "birth_place": [r"lugar de nacimiento", r"place of birth"],
    "gender": [r"sexo", r"género", r"sex", r"gender"],
    "height": [r"estatura", r"height"],
    "blood_type": [r"[ABO][\+\-]"],  # Solo formatos O+, A-, B+, AB-, etc.
    "issue_date": [r"fecha de expedici[oó]n", r"issue date"],
    "issue_place": [r"lugar de expedici[oó]n", r"place of issue"]
}

SPECIFIC_REGEX = {
    "document_number": r"\b(?:NUIP|No\.?|Núm(?:ero)?)[:\s\-]*([0-9\.]+)\b",
    "birth_date": r"(\d{2}[\/\-]\d{2}[\/\-]\d{4})",
    "birth_date_alt": r"(\d{2}\s?[A-Z]{3}\s?\d{4})",
    "height": r"\b(\d{1}[\.,]\d{2})\b",
    "blood_type": r"\b([ABO][\+\-])\b",
    "gender": r"\b([MF])\b",
    "last_name": r"Apellidos?[:\s]*([A-ZÑÁÉÍÓÚ ]+)",
    "first_name": r"Nombres?[:\s]*([A-ZÑÁÉÍÓÚ ]+)",
    "birth_place": r"Lugar[ ]?de[ ]?nacimiento[:\s]*([A-ZÑÁÉÍÓÚ ]+)",
    "issue_date_alt": r"(\d{2}[A-Z]{3}\d{2,4})"
}

MONTHS_ES = {
    "ENE": "01", "FEB": "02", "MAR": "03", "ABR": "04",
    "MAY": "05", "JUN": "06", "JUL": "07", "AGO": "08",
    "SEP": "09", "OCT": "10", "NOV": "11", "DIC": "12"
}

def parse_spanish_date(date_str):
    match = re.match(r"(\d{2})\s?([A-Z]{3})\s?(\d{2,4})", date_str.upper())
    if match:
        d, mon, y = match.groups()
        mon = MONTHS_ES.get(mon[:3], "00")
        if len(y) == 2:
            y = '20' + y
        return f"{y}-{mon}-{d}"
    return date_str


def extract_fields(text):
    fields = {k: "" for k in GENERIC_FIELDS}
    lines = text.splitlines()

    # 1) Extracción con regex específicos
    for key, pattern in SPECIFIC_REGEX.items():
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            val = m.group(1).strip().replace(",", ".")
            if key == "birth_date":
                d, mo, y = re.split(r"[\/\-]", val)
                val = f"{y}-{mo}-{d}"
            elif key == "birth_date_alt":
                val = parse_spanish_date(val)
                key = "birth_date"
            elif key == "height" and len(val) == 3:
                val = f"{val[0]}.{val[1:]}"
            elif key == "gender":
                val = "F" if "F" in val.upper() else ("M" if "M" in val.upper() else "")
            fields[key] = val

    # 2) Nombres, apellidos y lugar de nacimiento específicos
    for key in ("last_name", "first_name", "birth_place"):  
        if not fields[key] and key in SPECIFIC_REGEX:
            m = re.search(SPECIFIC_REGEX[key], text, re.IGNORECASE)
            if m:
                fields[key] = m.group(1).strip().title()

    # 3) Lugar de nacimiento genérico
    if not fields["birth_place"]:
        for idx, line in enumerate(lines):
            if re.search(r"lugar[ ]?de[ ]?nacimiento", line, re.IGNORECASE):
                if idx+1 < len(lines):
                    fields["birth_place"] = lines[idx+1].strip().title()
                break

    # 4) Fecha y lugar de expedición
    for i, line in enumerate(lines):
        if "expedicion" in line.lower().replace(" ", ""):
            nxt = lines[i+1] if i+1 < len(lines) else ""
            m = re.search(SPECIFIC_REGEX["issue_date_alt"], nxt, re.IGNORECASE)
            if m:
                fields["issue_date"] = parse_spanish_date(m.group(1))
            loc = re.sub(r"^\d{2}[A-Z]{3}\d{2,4}", "", nxt.strip(), flags=re.IGNORECASE)
            fields["issue_place"] = loc.strip().title()
            break

    # 5) Extracción genérica restante (incluye blood_type)
    for idx, line in enumerate(lines):
        for key, labels in GENERIC_FIELDS.items():
            if fields[key]: continue
            for lbl in labels:
                if re.search(lbl, line, re.IGNORECASE):
                    inline = re.search(rf"{lbl}\s*[:\-]?\s*([A-Za-z0-9ÁÉÍÓÚÑáéíóúñ\./ +\-]+)", line, re.IGNORECASE)
                    val = inline.group(1).strip() if inline else (lines[idx+1].strip() if idx+1<len(lines) else "")
                    if key == "document_number": val = val.replace(" ", "")
                    if key == "gender":
                        val = "F" if "F" in val.upper() else ("M" if "M" in val.upper() else "")
                    fields[key] = val
                    break

    # 6) Fallback número de documento
    if not fields["document_number"]:
        m = re.search(r"\b(?:nuip|no\.?)[ :\-]*([0-9\.]+)", text, re.IGNORECASE)
        if m: fields["document_number"] = m.group(1).strip()

    return fields

# ───── Pipeline principal ─────
def process_document(file_b64, file_name=""):
    try:
        data = decode_base64(file_b64)
        is_pdf = file_name.lower().endswith(".pdf")
        text = extract_text_from_pdf(data) if is_pdf else extract_text_from_image(data)
        if not text.strip():
            raise ValueError("No se extrajo texto del documento")
        doc_type = validate_document_type(text)
        fields = extract_fields(text)
        return doc_type, text, fields
    except Exception as e:
        print(f"Error processing documento: {str(e)}")
        return "Unknown", "", {}
