"""
Local Document Processing Tools
Handles PDF, DOCX, and other document formats locally
"""
import os
from typing import List, Optional
from pathlib import Path
from langchain.tools import BaseTool
from pydantic import Field

# Document loaders
try:
    from pypdf import PdfReader
    from docx import Document as DocxDocument
except ImportError:
    PdfReader = None
    DocxDocument = None


class ReadPDFTool(BaseTool):
    """Tool for reading and extracting text from PDF files"""
    
    name: str = "read_pdf"
    description: str = """
    Read and extract text content from a PDF file.
    Input should be the full path to the PDF file.
    Returns the extracted text content.
    """
    
    def _run(self, file_path: str) -> str:
        """Extract text from PDF"""
        try:
            if not os.path.exists(file_path):
                return f"Error: File not found at {file_path}"
            
            if not file_path.lower().endswith('.pdf'):
                return f"Error: File must be a PDF. Got: {file_path}"
            
            if PdfReader is None:
                return "Error: pypdf not installed. Run: pip install pypdf"
            
            reader = PdfReader(file_path)
            
            text_content = []
            for page_num, page in enumerate(reader.pages, 1):
                text = page.extract_text()
                text_content.append(f"--- Page {page_num} ---\n{text}\n")
            
            full_text = "\n".join(text_content)
            
            # Truncate if too long
            if len(full_text) > 10000:
                return f"{full_text[:10000]}\n\n[Content truncated - total {len(full_text)} characters, {len(reader.pages)} pages]"
            
            return full_text
            
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
    
    async def _arun(self, file_path: str) -> str:
        return self._run(file_path)


class ReadDOCXTool(BaseTool):
    """Tool for reading DOCX files"""
    
    name: str = "read_docx"
    description: str = """
    Read and extract text content from a DOCX (Word) file.
    Input should be the full path to the DOCX file.
    Returns the extracted text content.
    """
    
    def _run(self, file_path: str) -> str:
        """Extract text from DOCX"""
        try:
            if not os.path.exists(file_path):
                return f"Error: File not found at {file_path}"
            
            if not file_path.lower().endswith('.docx'):
                return f"Error: File must be a DOCX. Got: {file_path}"
            
            if DocxDocument is None:
                return "Error: python-docx not installed. Run: pip install python-docx"
            
            doc = DocxDocument(file_path)
            
            text_content = []
            for para in doc.paragraphs:
                if para.text.strip():
                    text_content.append(para.text)
            
            full_text = "\n\n".join(text_content)
            
            # Truncate if too long
            if len(full_text) > 10000:
                return f"{full_text[:10000]}\n\n[Content truncated - total {len(full_text)} characters]"
            
            return full_text
            
        except Exception as e:
            return f"Error reading DOCX: {str(e)}"
    
    async def _arun(self, file_path: str) -> str:
        return self._run(file_path)


class ListDocumentsTool(BaseTool):
    """Tool for listing available documents in a directory"""
    
    name: str = "list_documents"
    description: str = """
    List all documents (PDF, DOCX, TXT) in the documents directory.
    Input can be empty or a subdirectory path.
    Returns a list of available documents with their paths.
    """
    
    documents_path: str = Field(default="./data/documents")
    
    def _run(self, subdirectory: str = "") -> str:
        """List documents in directory"""
        try:
            base_path = Path(self.documents_path)
            
            if subdirectory:
                search_path = base_path / subdirectory
            else:
                search_path = base_path
            
            if not search_path.exists():
                return f"Directory not found: {search_path}"
            
            # Supported document types
            extensions = ['.pdf', '.docx', '.txt', '.doc']
            
            documents = []
            for ext in extensions:
                documents.extend(search_path.rglob(f'*{ext}'))
            
            if not documents:
                return f"No documents found in {search_path}"
            
            result = f"Found {len(documents)} document(s):\n\n"
            for doc in sorted(documents):
                size = doc.stat().st_size / 1024  # KB
                result += f"- {doc.name} ({size:.1f} KB)\n  Path: {doc}\n"
            
            return result
            
        except Exception as e:
            return f"Error listing documents: {str(e)}"
    
    async def _arun(self, subdirectory: str = "") -> str:
        return self._run(subdirectory)


class ReadTextFileTool(BaseTool):
    """Tool for reading plain text files"""
    
    name: str = "read_text_file"
    description: str = """
    Read content from a plain text file (.txt, .md, .csv, etc.).
    Input should be the full path to the text file.
    Returns the file content.
    """
    
    def _run(self, file_path: str) -> str:
        """Read text file"""
        try:
            if not os.path.exists(file_path):
                return f"Error: File not found at {file_path}"
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Truncate if too long
            if len(content) > 10000:
                return f"{content[:10000]}\n\n[Content truncated - total {len(content)} characters]"
            
            return content
            
        except Exception as e:
            return f"Error reading text file: {str(e)}"
    
    async def _arun(self, file_path: str) -> str:
        return self._run(file_path)


def create_document_tools() -> List[BaseTool]:
    """
    Create and return all document processing tools
    
    Returns:
        List of document tools ready to use with LangChain agents
    """
    return [
        ListDocumentsTool(),
        ReadPDFTool(),
        ReadDOCXTool(),
        ReadTextFileTool()
    ]


# For testing
if __name__ == "__main__":
    tools = create_document_tools()
    
    # Test listing documents
    list_tool = tools[0]
    result = list_tool.run("")
    print("Documents:")
    print(result)
