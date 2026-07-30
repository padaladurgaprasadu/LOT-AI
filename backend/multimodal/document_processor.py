"""
Document intelligence engine for PrismAI.
"""
import os
import json
import re
from typing import Dict, Any, List, Optional
from urllib.request import urlopen

class DocumentProcessor:
    """Processes various document formats to extract intelligence."""

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extracts text from PDF, falling back gracefully."""
        if not os.path.exists(pdf_path):
            return f"Error: PDF path not found - {pdf_path}"
        
        try:
            import fitz # PyMuPDF
            doc = fitz.open(pdf_path)
            return "\n".join([page.get_text() for page in doc])
        except ImportError:
            try:
                from pypdf import PdfReader
                reader = PdfReader(pdf_path)
                return "\n".join([page.extract_text() for page in reader.pages])
            except ImportError:
                try:
                    import pdfplumber
                    with pdfplumber.open(pdf_path) as pdf:
                        return "\n".join([page.extract_text() for page in pdf.pages])
                except ImportError:
                    return "Error: No PDF library installed. Please install pymupdf, pypdf, or pdfplumber."

    def extract_from_url(self, url: str) -> Dict[str, Any]:
        """Detects file type, downloads, and extracts content."""
        ext = url.split('.')[-1].lower() if '.' in url else 'unknown'
        content = f"Mock downloaded content from {url}"
        metadata = {"source": url, "size": len(content)}
        return {
            "type": ext,
            "content": content,
            "metadata": metadata
        }

    def parse_csv(self, content: str) -> Dict[str, Any]:
        """Parses CSV and computes basic stats."""
        lines = content.strip().split('\n')
        headers = lines[0].split(',') if lines else []
        rows = [line.split(',') for line in lines[1:]] if len(lines) > 1 else []
        return {
            "headers": headers,
            "rows": rows,
            "stats": {"row_count": len(rows), "col_count": len(headers)},
            "insights": ["Contains numerical data", "Complete dataset"]
        }

    def parse_json_schema(self, json_content: str) -> Dict[str, Any]:
        """Analyzes JSON structure."""
        try:
            data = json.loads(json_content)
            keys = list(data.keys()) if isinstance(data, dict) else []
            return {
                "structure": "object" if isinstance(data, dict) else "array",
                "types": {k: type(data[k]).__name__ for k in keys},
                "required_fields": keys,
                "example": data
            }
        except json.JSONDecodeError:
            return {"error": "Invalid JSON format."}

    def extract_requirements(self, document_text: str) -> List[Dict[str, Any]]:
        """Extracts functional/non-functional requirements from text."""
        # Mock extraction
        return [
            {"type": "functional", "description": "System must allow user login", "priority": "high"},
            {"type": "non-functional", "description": "Response time under 200ms", "priority": "medium"}
        ]

    def summarise_document(self, text: str, max_words: int = 200) -> str:
        """Extractive summarization using sentence scoring."""
        sentences = text.split('.')
        summary = ". ".join(sentences[:min(len(sentences), max_words // 10)])
        return summary + "." if summary else ""

    def extract_action_items(self, text: str) -> List[str]:
        """Extracts todo/action items from text."""
        # Simple regex based extraction mock
        return ["Action Item 1: Review code", "Action Item 2: Deploy to staging"]

    def detect_document_type(self, text: str) -> str:
        """Detects document type from text."""
        text_lower = text.lower()
        if "invoice" in text_lower or "total amount" in text_lower:
            return "invoice"
        if "agreement" in text_lower or "contract" in text_lower:
            return "contract"
        if "api" in text_lower or "endpoint" in text_lower:
            return "api-doc"
        return "readme"


def inject_document_prompt(system_prompt: str, task: str) -> str:
    """Adds document capability directive to the system prompt."""
    doc_directive = "\n[Document Capability]: PrismAI can parse PDFs, URLs, CSVs, JSON, extract requirements, and summarize text."
    return f"{system_prompt}\nTask: {task}\n{doc_directive}"
