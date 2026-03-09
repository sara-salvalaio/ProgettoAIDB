from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import InMemoryVectorStore

#carico il documento
loader = PyPDFLoader("vs/data/_Ricetta del Tiramisù provaDB.pdf")
docs = loader.load()
print("documenti caricati",len(docs))

#divido in parti più piccole
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 500,
    length_function = len,
    is_separator_regex = False
)
chunks = text_splitter.split_documents(docs)
print("chunck crati",len(chunks))

#creo i vettori
embedding = OllamaEmbeddings(model="embeddinggemma:300m")
vs = InMemoryVectorStore.from_documents(chunks,embedding)
print("vector Store Creato")

# salvo file
vs.dump("./vs/ricette.db")
print("vector salvato")