from PyPDF2 import PdfReader
import docx2txt

def get_texts_from_files(files):
    docFiles = []
    pdfFiles = []

    for file in files:
        fileName = str(file.name)
        if ".docx" in fileName:
            docFiles.append(file)
        elif ".pdf" in fileName:
            pdfFiles.append(file)
    text = get_pdf_texts(pdfFiles)
    text += get_doc_texts(docFiles)
    return text
        
def get_pdf_texts(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    
    return text


def get_doc_texts(docs):
    text = ""
    for doc in docs:
        text += docx2txt.process(doc)
    return text
