import streamlit as st
import os
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import re

# Configuración de rutas
PDF_OUTPUT = "escritura.pdf"
TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\Users\USER\Downloads\poppler-24.08.0\Library\bin"
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

# Palabras clave para detectar linderos
PALABRAS_CLAVE = [
    "linderos", "colinda", "colindando", "delimitado", "cabida", "área", "area",
    "SUR", "NORTE", "ORIENTE", "OCCIDENTE", "PONIENTE", "LEVANTE",
    "nororiente", "noroccidente", "suroriente", "suroccidente"
]

def eliminar_encabezados(texto):
    lineas = texto.splitlines()
    lineas_filtradas = [linea for linea in lineas if not re.search(r'Lote|Etapa|Parcela|Predio|No\. \d+', linea, re.IGNORECASE)]
    return "\n".join(lineas_filtradas)

def extraer_linderos(texto):
    secciones = []
    parrafo_actual = ""
    for linea in texto.splitlines():
        parrafo_actual += " " + linea.strip()
        if any(palabra in linea.lower() for palabra in PALABRAS_CLAVE):
            secciones.append(parrafo_actual.strip())
            parrafo_actual = ""
    return "\n\n".join(secciones)

def procesar_pdf(ruta_pdf):
    texto_extraido = ""
    imagenes = convert_from_path(ruta_pdf, 300, poppler_path=POPPLER_PATH)
    for i, img in enumerate(imagenes):
        texto = pytesseract.image_to_string(img, lang="spa")
        texto_limpio = eliminar_encabezados(texto)
        texto_extraido += f"\n\n{texto_limpio}"
    return texto_extraido

# Interfaz Streamlit
st.set_page_config(page_title="Extracción de Linderos", layout="wide")
st.title("📜 Extracción de Linderos de Escrituras Públicas")

uploaded_file = st.file_uploader("Sube un archivo PDF de la escritura", type=["pdf"])

if uploaded_file:
    with open(PDF_OUTPUT, "wb") as f:
        f.write(uploaded_file.read())

    st.info("Procesando el archivo, por favor espera...")
    texto_completo = procesar_pdf(PDF_OUTPUT)

    with st.expander("📃 Texto completo extraído"):
        st.text_area("Texto OCR", texto_completo, height=400)

    linderos = extraer_linderos(texto_completo)
    st.subheader("📍 Linderos detectados (literal):")
    st.text_area("Linderos", linderos, height=300)