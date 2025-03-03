import os
from dotenv import load_dotenv

load_dotenv()

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import ReadTheDocsLoader, TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"), model="text-embedding-3-small")

def ingest_docs():
    
    #loader = ReadTheDocsLoader("/Users/felipe/Development/en.ahmedali.txt")
    loader = TextLoader("./bible.txt")

    raw_documents = loader.load()
    print(f"loaded {len(raw_documents)} documents")

    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=60)
    documents = splitter.split_documents(raw_documents)

    for doc in documents:
        new_url = doc.metadata["source"]
        #new_url = new_url.replace("langchain-docs", "https:/")
        doc.metadata.update({"source": new_url})

    print(f"Going to add {len(documents)} to Pinecone")
    PineconeVectorStore.from_documents(documents, embeddings, index_name=os.getenv("PINECONE_INDEX_NAME"))

    print("Loading to vedtor store done")



if __name__ == "__main__":
    ingest_docs()
    print("Ingestion complete")

