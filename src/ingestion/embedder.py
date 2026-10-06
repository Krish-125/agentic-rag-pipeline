from langchain_huggingface import HuggingFaceEmbeddings

def get_embeddings(model_name: str = "BAAI/bge-small-en-v1.5") -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name=model_name,
        encode_kwargs={"normalize_embeddings": True}
    )

# if __name__ == "__main__":
#     embeddings = get_embeddings()
#     vector = embeddings.embed_query("What is the refund policy?")
#     print(f"Vector length: {len(vector)}")
#     print(f"First 5 values: {vector[:5]}")