import os
from typing import Any, Dict, List
from dotenv import load_dotenv
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains import create_history_aware_retriever
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

load_dotenv()


#INDEX_NAME = "langchain-docs-index"
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

def run_llm(query:str, chat_history: List[Any] = []) -> List[Any]:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    docsearch = PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings)

    chat = ChatOpenAI(verbose=True, temperature=0)

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

    stuff_documents_chain = create_stuff_documents_chain(chat, retrieval_qa_chat_prompt)

    rephrase_qa_chat_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")

    history_aware_retriever = create_history_aware_retriever(llm=chat, retriever=docsearch.as_retriever(), prompt=rephrase_qa_chat_prompt)

    qa = create_retrieval_chain(
        retriever=history_aware_retriever, combine_docs_chain=stuff_documents_chain
    )

    result = qa.invoke(input={"input": query, "chat_history": chat_history})
    new_result = {
        "query": result["input"],
        "result": result["answer"],
        "source_documents": result["context"]
    }
    return new_result

if __name__ == "__main__":
    result = run_llm("What is Langchain chain?")
    print(result["result"])   