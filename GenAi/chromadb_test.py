import chromadb

client = chromadb.Client()
collection = client.create_collection("test")

collection.add(
    documents=["test"],
    embeddings=[[0.1, 0.2]],
    ids=["id1"]  # unique ID per document
)

results = collection.query(
    query_embeddings=[[0.1, 0.2]],
    n_results=1
)

print(results)
