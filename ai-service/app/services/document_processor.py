import io
from pypdf import PdfReader
from docx import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentProcessor:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        # RecursiveCharacterTextSplitter keeps paragraphs/sentences intact
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )

    async def extract_text(self, file_bytes: bytes, filename: str) -> str:
        """Extracts plain text from PDF, DOCX, or TXT files."""
        text = ""
        file_ext = filename.split(".")[-1].lower()

        if file_ext == "pdf":
            pdf_reader = PdfReader(io.BytesIO(file_bytes))
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"

        elif file_ext == "docx":
            doc = Document(io.BytesIO(file_bytes))
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"

        elif file_ext == "txt":
            text = file_bytes.decode("utf-8")

        else:
            raise ValueError(f"Unsupported file format: .{file_ext}")

        return text

    def create_chunks(self, text: str) -> list[str]:
        """Splits raw text into manageable chunks."""
        return self.text_splitter.split_text(text)