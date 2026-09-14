from langchain_core.documents import Document
from docx import Document as DocxDocument
import pdfplumber
import json
import os

# Load PDF file and extract text and tables into Document objects using PDFPlumber. 
# Each page's text and tables are stored as separate Document objects with metadata 
# including the source filename, page number, and content type (text or table).

def load_pdf(filepath:str) -> list[Document]:
    filename = os.path.basename(filepath)
    documents = []

    with pdfplumber.open(filepath) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text and text.strip():
                metadata = {
                    "source_filename": filename,
                    "page_number": page_number,
                    "content_type": "text"
                }
                documents.append(Document(page_content=text, metadata=metadata))

            tables = page.extract_tables()
            for t_idx, table in enumerate(tables):
                if not table and len(table) < 2:
                    continue
                headers = table[0]
                table_text = f"Table {t_idx + 1} on page {page_number}:\n"
                for row in table[1:]:
                    row_description = ", ".join(
                        f"{headers[i]} = {row[i]}" for i in range(len(headers)) if i < len(row) and row[i]
                    )
                    table_text += f"- {row_description}\n"
                metadata = {
                    "source_filename": filename,
                    "page_number": page_number,
                    "content_type": "table"
                }
                documents.append(Document(page_content=table_text, metadata=metadata))
    return documents

# Load DOCX file and extract text into Document objects using python-docx.
def load_docx(filepath:str) -> list[Document]:
    filename = os.path.basename(filepath)
    documents = []
    doc = DocxDocument(filepath)

    full_text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    if full_text.strip():
        metadata = {
            "source_filename": filename,
            "content_type": "text"
        }
        documents.append(Document(page_content=full_text, metadata=metadata))

    for t_idx, table in enumerate(doc.tables):
        rows = [[cell.text.strip() for cell in row.cells] for row in table.rows]
        if len(rows) < 2:
            continue

        headers = rows[0]
        table_text = f"Table {t_idx + 1}:\n"
        for row in rows[1:]:
            row_description = ", ".join(
                f"{headers[i]} = {row[i]}" for i in range(len(headers)) if i < len(row) and row[i]
            )
            table_text += f"- {row_description}\n"
        metadata = {
            "source_filename": filename,
            "content_type": "table"
        }
        documents.append(Document(page_content=table_text, metadata=metadata))

    return documents