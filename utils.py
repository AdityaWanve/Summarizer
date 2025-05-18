import PyPDF2
from docx import Document
from io import BytesIO

def extract_text_from_pdf(file_bytes):
    reader = PyPDF2.PdfReader(BytesIO(file_bytes))
    text = []
    for page in reader.pages:
        text.append(page.extract_text())
    return "\n".join(text)

def extract_text_from_docx(file_bytes):
    doc = Document(BytesIO(file_bytes))
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return "\n".join(text)
