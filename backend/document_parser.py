import PyPDF2
import docx
from typing import List

class DocumentParser:
    @staticmethod
    def parse_pdf(file_path: str) -> str:
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except:
            text = "Error reading PDF"
        return text
    
    @staticmethod
    def parse_docx(file_path: str) -> str:
        try:
            doc = docx.Document(file_path)
            return "\n".join([paragraph.text for paragraph in doc.paragraphs])
        except:
            return "Error reading DOCX"
    
    @staticmethod
    def parse_txt(file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except:
            return "Error reading TXT"
    
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
        return chunks if chunks else ["No content to process"]