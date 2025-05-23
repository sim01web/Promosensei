import faiss
import os
import pickle
from sentence_transformers import SentenceTransformer
from scraper import scrape_all_offers 
# Dimension for MiniLM model embeddings
VECTOR_DIM = 384  

def embed_offers(offers, model_name='all-MiniLM-L6-v2'):
    model = SentenceTransformer(model_name)
    texts = [f"{offer['title']} {offer['description']}" for offer in offers]
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings

def save_vector_db(embeddings, offers, db_path="faiss_index"):
    index = faiss.IndexFlatL2(VECTOR_DIM)
    index.add(embeddings)

    os.makedirs(db_path, exist_ok=True)

    # Saving FAISS index
    faiss.write_index(index, f"{db_path}/offers.index")

    # Saving metadata
    with open(f"{db_path}/offers_meta.pkl", "wb") as f:
        pickle.dump(offers, f)

    print(f"Saved {len(offers)} offers to vector DB at '{db_path}'.")

def ingest():
    offers = scrape_all_offers()  
    if not offers:
        print("No offers found.")
        return

    embeddings = embed_offers(offers)
    save_vector_db(embeddings, offers)

if __name__ == "__main__":
    ingest()
