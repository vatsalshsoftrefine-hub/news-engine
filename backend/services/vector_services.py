import chromadb
from sentence_transformers import SentenceTransformer

# Initialize embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize ChromaDB client
client = chromadb.Client()

# Create or get collection
collection = client.get_or_create_collection(name="news")


def generate_embedding(text):
    """
    Convert text to embedding vector
    """
    return model.encode(text).tolist()


def add_to_vector_db(article):
    """
    Store article in vector DB
    """

    text = f"{article.get('title')} {article.get('description')}"

    embedding = generate_embedding(text)

    collection.add(
        documents=[text],
        embeddings=[embedding],
        ids=[article.get("id")],
        metadatas=[{
            "title": article.get("title"),
            "link": article.get("link"),
            "category": article.get("category")
        }]
    )