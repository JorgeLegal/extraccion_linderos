import os
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import re

# 📁 Rutas
PDF_PATH = 'escritura.pdf'  # Tu archivo PDF
POPPLER_PATH = r'C:\Users\USER\Downloads\poppler-24.08.0\Library\bin'  
TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
OUTPUT_TXT = 'texto_extraido.txt'

# ⚙️ Configuraciones
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

# 🧽 Limpieza de encabezados repetitivos
def limpiar_encabezado(texto):
    patron = r"(República\s+de\s+Colombia.*?cadena.*?(\n|$))|(Pág\.\s*\d+)|(\d{4,})"
    return re.sub(patron, '', texto, flags=re.IGNORECASE)

# 🔍 Expresiones para detectar cabida y linderos
PATRON_CLAVES = re.compile(
    r"(cabida|área|superficie|extensión|comprendido dentro de|medidas|metraje|"
    r"lindero[s]?|colind[aeo][ns]?|mojón|lado|norte|sur|oriente|occidente|"
    r"suroriente|suroccidente|dirección|hasta|inicia|continúa|distancia|metros|cent[íi]metros|dec[íi]metros)",
    re.IGNORECASE
)

# 🔄 Convertir PDF a imágenes
print(f"📄 Convirtiendo '{PDF_PATH}' a imágenes...")
pages = convert_from_path(PDF_PATH, 300, poppler_path=POPPLER_PATH)

texto_completo = ""
print("🧠 Ejecutando OCR...")
for i, page in enumerate(pages):
    text = pytesseract.image_to_string(page, lang='spa')
    text = limpiar_encabezado(text)
    texto_completo += text + "\n"
    print(f"✅ Página {i+1} procesada")

# 🧠 Extraer párrafos que contengan las palabras clave (cabida y linderos)
parrafos = re.split(r"\n\s*\n", texto_completo)
extraidos = []
for p in parrafos:
    if PATRON_CLAVES.search(p):
        extraidos.append(p.strip())

# 📝 Guardar texto extraído
with open(OUTPUT_TXT, 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(extraidos))

print(f"\n✅ Texto extraído y guardado en: {OUTPUT_TXT}")