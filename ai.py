from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


# Inizializza il modello AI
from langchain_ollama import ChatOllama
print("Carico modello...")
lcmodel = ChatOllama(model="gemma3:4b", temperature=0, reasoning=False)
print("Modello caricato.")


from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
embedding = OllamaEmbeddings(model="embeddinggemma:300m")
vs = InMemoryVectorStore.load("./vs/ricette.db", embedding)
retriever = vs.as_retriever()

#carico il documento
loader = PyPDFLoader("vs/data/ricettarioDB.pdf")
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


print("creo contesto")
# Context condiviso 
context = [
    ('system', 'sei un cuoco che conosce tutti le ricette a memoria e sa come abbinare bene gli ingredienti'),
    ('system', '')
]
lcmodel.invoke(context) 

print("contesto creato")


#utilizziamo il rag
doc_texts = "\n".join(chunk.page_content for chunk in chunks)
doc_texts = """
-- TABELLA CATEGORIA
CREATE TABLE Categoria (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL
);

INSERT INTO CATEGORIA (nome) VALUES ("primo", "secondo", "contorno", "dessert")
-- TABELLA RICETTA
CREATE TABLE Ricetta (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(150) NOT NULL,
    descrizione TEXT,
    tempo INT,
    difficolta VARCHAR(50),
    categoria_id INT,
    FOREIGN KEY (categoria_id) REFERENCES Categoria(id)
);
-- TABELLA INGREDIENTI
CREATE TABLE Ingredienti (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL
);
-- TABELLA RICETTEINGREDIENTI
CREATE TABLE RicetteIngredienti (
    ricetta_id INT,
    ingrediente_id INT,
    qta DECIMAL(10,2),
    u_misura VARCHAR(50),
    PRIMARY KEY (ricetta_id, ingrediente_id),
    FOREIGN KEY (ricetta_id) REFERENCES Ricetta(id),
    FOREIGN KEY (ingrediente_id) REFERENCES Ingredienti(id)
);
-- TABELLA PREPARAZIONE
CREATE TABLE Preparazione (
    id INT PRIMARY KEY AUTO_INCREMENT,
    ricetta_id INT,
    descrizione TEXT,
    progressivo INT,
    FOREIGN KEY (ricetta_id) REFERENCES Ricetta(id)
);
"""
context[1] = ('system', doc_texts)

domanda = "descrivi la ricetta a te data, descrivenedo la difficolta, gli ingredienti, il procedimento e il tempo di preparazione aggiungendo anche la categoria di appartenenza di questa ricetta. In piu aggiungi anche dele query legate alla ricetta e delle insert. Infine scrivi tutti i dati in formato tabulare (tipo schema database)"

print(f"Domamda >>  {domanda}")

context.append(('human', domanda))

response  = lcmodel.invoke(context)
context.append(('ai', response.content))


print(f"Risposta AI >> {response.content}")