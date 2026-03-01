import os
import sys
import pandas as pd
import logging

# Add the Backend directory to the Python path so we can import rag modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag.local_pdf_retriever import _load_pdf, _chunk_pages, _compute_embeddings
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

def generate_embeddings_excel():
    # Setup paths
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    load_dotenv(os.path.join(backend_dir, ".env"))
    
    pdf_path = os.path.join(backend_dir, "data", "legal_document.pdf")
    output_excel = os.path.join(backend_dir, "legal_document_embeddings.xlsx")
    
    if not os.path.exists(pdf_path):
        logger.error(f"PDF not found at {pdf_path}")
        return

    logger.info("Step 1: Loading PDF and extracting text...")
    pages = _load_pdf(pdf_path)
    
    if not pages:
        logger.error("No text could be extracted from the PDF.")
        return
        
    logger.info("Step 2: Chunking text...")
    chunks = _chunk_pages(pages, chunk_size=512, overlap=50)
    
    logger.info("Step 3: Generating vector embeddings...")
    # This calls the HF Inference API through get_shared_embedding_model()
    embeddings_matrix = _compute_embeddings(chunks)
    
    logger.info(f"Step 4: Preparing data for Excel export...")
    data = []
    
    for i, chunk in enumerate(chunks):
        # Convert the dense numpy array (e.g., shape 384 or 768) into a comma-separated string 
        # or a JSON array string so it fits easily into an Excel cell.
        embedding_list = embeddings_matrix[i].tolist()
        embedding_str = str(embedding_list)
        
        data.append({
            "Chunk ID": i + 1,
            "Page Number": chunk["page"],
            "Character Start": chunk.get("char_start", 0),
            "Text Snippet": chunk["text"],
            "Vector Dimensions": len(embedding_list),
            "Embedding Vector": embedding_str
        })
        
    df = pd.DataFrame(data)
    
    logger.info(f"Step 5: Saving {len(df)} rows to Excel...")
    df.to_excel(output_excel, index=False)
    
    logger.info(f"✅ Success! Embeddings saved to: {output_excel}")

if __name__ == "__main__":
    generate_embeddings_excel()
