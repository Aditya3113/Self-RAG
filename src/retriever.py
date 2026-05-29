import src.config 

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

urls = [
    "https://ryanocm.substack.com/p/123-how-tiny-experiments-can-lead",
    "https://ryanocm.substack.com/p/122-life-razor-the-one-sentence-that",
    "https://ryanocm.substack.com/p/121-warren-buffetts-255-strategy",
    "https://ryanocm.substack.com/p/120-30-years-on-earth-11-habits-that",
]

print("Loading documents into the knowledge base...")
docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=250, 
    chunk_overlap=0
)
doc_splits = text_splitter.split_documents(docs_list)

vectorstore = Chroma.from_documents(
    documents=doc_splits,
    collection_name="rag-chroma",
    embedding=OpenAIEmbeddings(),
)

retriever = vectorstore.as_retriever()