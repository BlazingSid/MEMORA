from app.core.llm import generate_response


response = generate_response(
    "Explain what a vector database is in one simple sentence."
)

print("\nMEMORA LLM RESPONSE:\n")
print(response)
