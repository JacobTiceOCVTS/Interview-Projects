import asyncio
import os
from pypdf import PdfReader
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# document that rag will interpret
DOCUMENT_DIR_PATH = "./Files/documents"
TEXT_FILES = "./Files/data/"

for file in os.listdir(TEXT_FILES):
    os.remove(f"{TEXT_FILES}/{file}")
    print(f"Removed file: {TEXT_FILES}/{file}")
if len(os.listdir(TEXT_FILES)) < 1:
    print("Cleared data to be read")

def convert_pdf_to_text(document_path):
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
        with open(TEXT_FILES, 'w', encoding='utf-8') as text_file:
            text_file.write(text_to_save)
        print(f"Succesfully saved text to {text_file}")
    except Exception as e:
        print(f"ERROR: Failed to save to file. Details: {e}")

def convert_documents_to_text(docuements_dir):
    pdfs = os.listdir(docuements_dir)
    i = 0
    for pdf in pdfs:
        try:
            reader = PdfReader(f"{DOCUMENT_DIR_PATH}/{pdf}")
            text_to_save = ""
            for page in reader.pages:
                text_to_save += page.extract_text() + "\n"
            print(f"Successfully extracted {len(text_to_save)} characters from the text")
        except Exception as e:
            print(f"ERROR: Document could not be interpreted {e}")
            return
        try:
            with open(f"{TEXT_FILES}/text{i}", 'w', encoding='utf-8') as text_file:
                text_file.write(text_to_save)
            print(f"Succesfully saved text to {TEXT_FILES}")
        except Exception as e:
            print(f"ERROR: Failed to save to file. Details: {e}")
        i += 1

Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
Settings.llm = Ollama(
    model="llama3.1",
    request_timeout=360.0,
    # Manually set the context window to limit memory usage
    context_window=8000,
)


convert_documents_to_text(DOCUMENT_DIR_PATH)
documents = SimpleDirectoryReader("./Files/data").load_data()
index = VectorStoreIndex.from_documents(
    documents,
    # we can optionally override the embed_model here
    # embed_model=Settings.embed_model,
)

query_engine = index.as_query_engine(
    # we can optionally override the llm here
    # llm=Settings.llm,
)

async def search_documents(query: str) -> str:
    """Useful for answering natural language questions about a personal essay written by Paul Graham."""
    response = await query_engine.aquery(query)
    return str(response)

agent = AgentWorkflow.from_tools_or_functions(
    [search_documents],
    llm=Settings.llm,
    system_prompt="""You are a helpful assistant that can search through documents to answer questions.""",
)

async def main():
    response = await agent.run(
        "How many documents did you load? Were they unique? If no, how many were copies?"
    )
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
    print("Yay")
