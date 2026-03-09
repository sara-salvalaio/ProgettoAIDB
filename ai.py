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
embedding = OllamaEmbeddings(model="embeddinggemma:300m")
vs = InMemoryVectorStore.load("./vs/ricette.db", embedding)
retriever = vs.as_retriever()


print("creo contesto")
# Context condiviso 
context = [
    ('system', 'sei uncuoco che conosce tutti le ricette a memoria e sa come abbinare bene gli ingredienti'),
    ('system', '')
]
lcmodel.invoke(context) 

print("contesto creato")



@app.route('/ProgettoAIDB', methods=['POST', 'OPTIONS'])
def aicompanion():
   if request.method == 'OPTIONS':
       response = make_response()
       response.headers['Access-Control-Allow-Origin'] = '*'
       response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
       response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
       return response
   
   question = request.get_json().get('message', '')
   print(question)
   context.append(('human', question))

   #utilizziamo il rag
   documents = retriever.invoke(question)
   doc_texts = "\n".join(doc.page_content for doc in documents)
   doc_texts= "usa questo contesto per rispondere e se non ci risci rispondi boh" + doc_texts
   context[1] = ('system', doc_texts)

   response  = lcmodel.invoke(context)
   context.append(('ai', response.content))


   # Aggiungi la risposta dell'AI al contesto
   # context.append(('ai', ai_response))
   return jsonify({
        'question': question,
        'answer': response.content
    })

if __name__ == '__main__':
    app.run(port=9000, debug=False)