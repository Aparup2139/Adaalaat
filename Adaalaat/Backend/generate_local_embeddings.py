import os
import sys
import pandas as pd
import logging
from sentence_transformers import SentenceTransformer

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from rag.local_pdf_retriever import _load_pdf, _chunk_pages

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

def generate_local_embeddings_excel():
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(backend_dir, "data", "legal_document.pdf")
    output_excel = os.path.join(backend_dir, "legal_document_embeddings.xlsx")
    
    if not os.path.exists(pdf_path):
        logger.error(f"PDF not found at {pdf_path}")
        return

    logger.info("Step 1: Loading PDF and extracting text...")
    pages = _load_pdf(pdf_path)
    
    if not pages:
        logger.error("No text extracted.")
        return
        
    logger.info("Step 2: Chunking text...")
    chunks = _chunk_pages(pages, chunk_size=512, overlap=50)
    texts = [c["text"] for c in chunks]
    
    logger.info(f"Step 3: Loading local embedding model (BAAI/bge-small-en-v1.5) ...")
    # This downloads the model to cache once, then runs entirely locally instantly
    model = SentenceTransformer('BAAI/bge-small-en-v1.5')
    
    logger.info(f"Step 4: Computing {len(texts)} embeddings locally (this will be fast)...")
    embeddings = model.encode(texts, normalize_embeddings=True)
    
    logger.info(f"Step 5: Preparing data for Excel export...")
    data = []
    
    for i, chunk in enumerate(chunks):
        embedding_list = embeddings[i].tolist()
        # Cap the display to avoid Excel cell limits if needed, but [] stringification is fine
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
    
    logger.info(f"Step 6: Saving {len(df)} rows to Excel...")
    df.to_excel(output_excel, index=False)
    
    logger.info(f"✅ Success! Local embeddings saved to: {output_excel}")

if __name__ == "__main__":
    generate_local_embeddings_excel()
