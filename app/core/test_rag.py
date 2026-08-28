from app.core.rag import ask_memora


question = "What have I learned about desktop applications?"

answer = ask_memora(question)

print("\nMEMORA:\n")
print(answer)
