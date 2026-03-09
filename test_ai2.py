from langchain_ollama import ChatOllama

lcmodel = ChatOllama(model = "gemma3:4b", temperature=0, reasoning=False)

context = [("system", "Tu sei un''intelligenza artificiale volta ad aiutare gli studenti di una classe dell’ITIS Zuccante ad essere promossi all''esame di Stato. Ti chiami Consigliere")]

context.append(("human","Come faccio ad essere promosso?"))

response = lcmodel.invoke(context)

context.append(("ai", response.content))

print(response.content)

context.append(("human","Ma io non voglio studiare"))

response = lcmodel.invoke(context)

context.append(("ai", response.content))

print(response.content)
