from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-m3")

sentences = [
    "The weather is lovely today.",
    "It's so sunny outside!",
    "He drove to the stadium."
]

embeddings = model.encode(sentences)
similarities = model.similarity(embeddings, embeddings)

print(similarities.shape)
