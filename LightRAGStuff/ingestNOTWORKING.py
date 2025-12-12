import asyncio
from lightrag import LightRAG, QueryParam
from lightrag.llm.ollama import ollama_model_complete
from lightrag.utils import EmbeddingFunc
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import torch

#document that rag will interpret
DOCUMENT_PATH = "document.pdf"
TEXT_FILE = "txt_to_ingest.txt"

#dir where rag will work inside
WORKING_DIR = "./rag_data"

# Initialize sentence transformer model on CPU
embedding_model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

def embed_texts(texts):
    """Embed texts using sentence-transformers (synchronous)"""
    if isinstance(texts, str):
        texts = [texts]
    # Return numpy array instead of list
    return embedding_model.encode(texts, convert_to_numpy=True)

async def async_embed_texts(texts):
    """Async wrapper for embedding function"""
    return embed_texts(texts)

async def rag_initialize():
    rag = LightRAG(
        working_dir=WORKING_DIR,
        llm_model_func=ollama_model_complete,
        llm_model_name="gemma3:12b",
        llm_model_kwargs={"host": "http://127.0.0.1:11434", "options": {"num_ctx": 32768}},
        embedding_func=EmbeddingFunc(
            embedding_dim=384,
            max_token_size=8192,
            func=async_embed_texts
        )
    )
    await rag.initialize_storages()
    return rag


async def convert_pdf_to_text(document_path):
    print(f"Starting ingestion for {document_path}")

    try:
        reader = PdfReader(document_path)
        text_to_save = ""
        for page in reader.pages:
            text_to_save += page.extract_text() + "\n"
        print(f"Successfully extracted {len(text_to_save)} characters from the text")
    except Exception as e:
        print(f"ERROR: Document could not be interpreted {e}")
        return
    
    try:
        with open(TEXT_FILE, 'w', encoding='utf-8') as text_file:
            text_file.write(text_to_save)
        print(f"Succesfully saved text to {TEXT_FILE}")
    except Exception as e:
        print(f"ERROR: Failed to save to file. Details: {e}")
    
async def main():
    rag = await rag_initialize()

    await convert_pdf_to_text(DOCUMENT_PATH)
    with open(TEXT_FILE, 'r', encoding="utf-8") as f:
        await rag.ainsert(f.read())

    resp = await rag.aquery(
        "What is the major theme in this story?",
        param=QueryParam(mode="global", stream=True)
    )

    print(resp)

if __name__ == "__main__":
    asyncio.run(main())
    print("Yay")